"""data creation pipeline"""

import os
import sys
# import pdb
import argparse
import logging
import concurrent.futures
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
from tqdm import tqdm

from utils import (
    load_json_file,
    load_pickle_file,
    dump_json_file,
    dump_pickle_file
)
from data_creation_utils import (
    annotate_all_subtrees,
    embed_all_subtrees,
    extract_all_subtrees
)
from llm_utils_new import LLMResponseManager, EmbeddingManager
from qd_train import merge_log_files, setup_logger


@dataclass
class ProcessedData:
    content: List[Dict[str, Any]]
    ids: List[str]
    subtrees: List[Dict[str, Any]]
    vectors: Dict[str, Any]


@dataclass
class Paths:
    split: str
    flat_split: str
    flat_split_embedding: str


def get_file_paths(
    dataset_name: str,
    split_info: Tuple[str, str, str],
    anonymization_key: str,
    anonymizer: str,
    q_decomposer: str
) -> Tuple[Paths, str]:
    split_name, split_split_name, split_mode = split_info
    common_prefix = "" if q_decomposer == "gpt4_0125" else f"{q_decomposer}_"

    base_path = f"data/{dataset_name}/decomposed"
    common_suffix = f"{split_name}_{split_split_name}_{split_mode}"

    split_path = f"{base_path}/{common_prefix}{common_suffix}"
    flat_split_path = f"{base_path}/{common_prefix}flat_{common_suffix}"
    flat_split_embedding_path = f"{base_path}/{common_prefix}flat_{common_suffix}"
    flat_split_embedding_path += (
        f"_template-{anonymization_key}-{anonymizer}_vectors"
        if anonymization_key else
        "_vectors"
    )
    log_file_path = f"data/{dataset_name}/LOGS/DATA_CREATION_PIPE_{common_prefix}_{common_suffix}"

    paths = Paths(split_path, flat_split_path, flat_split_embedding_path)
    return paths, log_file_path


def update_content(
    processed: ProcessedData, new_data: List[Dict[str, Any]],
    new_subtrees: List[Dict[str, Any]], new_vectors: Dict[str, Any],
    paths: Paths, file_suffix: str
):
    processed.content.extend(new_data)
    processed.ids.extend([item['qid'] for item in new_data])
    processed.subtrees.extend(new_subtrees)
    processed.vectors.update(new_vectors)

    dump_json_file(
        f"{paths.split}_{file_suffix}.json", processed.content
    )

    dump_json_file(
        f"{paths.flat_split}_{file_suffix}.json", processed.subtrees
    )

    # dump_pickle_file(
    #     f"{paths.flat_split_embedding}_{file_suffix}.pkl", processed.vectors
    # )


def process_item(
    item, anonymization_key, llm_manager, embed_manager, logger
):
    query_vectors = {}
    lst_sub_tree = []

    item_id = item['qid']
    decomposition_tree = item['decomposition']

    logger.info("processing item: %s", item_id)

    annotate_all_subtrees(
        decomposition_tree, item_id,
        anonymization_key, llm_manager, logger
    )

    # embedding_key = (
    #     f"template_{anonymization_key}_{llm_manager.model_name}"
    #     if anonymization_key else
    #     ""
    # )
    # embed_all_subtrees(decomposition_tree, embedding_key, query_vectors, embed_manager, logger)

    extract_all_subtrees(decomposition_tree, lst_sub_tree)

    return {'qid': item_id, 'query_vectors': query_vectors, 'lst_sub_tree': lst_sub_tree}


def process_dataset_parallel(
    data: List[Dict[str, Any]], processed: ProcessedData,
    llm_manager: LLMResponseManager, embed_manager: EmbeddingManager,
    anonymization_key: str, paths: Paths, file_suffix: str,
    main_logger: logging.Logger, num_workers: int, log_file_path: str
) -> None:
    loggers = [setup_logger(log_file_path, worker_id) for worker_id in range(num_workers)]

    new_data = []
    vectors_combined = {}
    subtrees_combined = []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [
                executor.submit(
                    process_item, item, anonymization_key,
                    llm_manager, embed_manager, loggers[idx % num_workers]
                )
                for idx, item in enumerate(data)
            ]

            data = {item['qid']: item for item in data}
            for future in tqdm(
                concurrent.futures.as_completed(futures), total=len(data), ncols=100
            ):
                result = future.result()
                item_id = result['qid']
                vectors = result['query_vectors']
                subtrees = result['lst_sub_tree']

                vectors_combined.update(vectors)
                subtrees_combined.extend(subtrees)
                new_data.append(data[item_id])
    except KeyboardInterrupt:
        update_content(
            processed, new_data,
            subtrees_combined, vectors_combined,
            paths, file_suffix
        )
        merge_log_files(num_workers, log_file_path, main_logger)
        sys.exit()
    update_content(
        processed, new_data,
        subtrees_combined, vectors_combined,
        paths, file_suffix
    )
    merge_log_files(num_workers, log_file_path, main_logger)


def process_dataset_sequential(
    data: List[Dict[str, Any]], processed: ProcessedData,
    llm_manager: LLMResponseManager, embed_manager: EmbeddingManager,
    anonymization_key: str, paths: Paths, file_suffix: str,
    main_logger: logging.Logger
) -> None:
    new_data = []
    vectors_combined = {}
    subtrees_combined = []
    try:
        for item in tqdm(data, total=len(data), ncols=100):
            result = process_item(
                item, anonymization_key, llm_manager, embed_manager, main_logger
            )
            vectors = result['query_vectors']
            subtrees = result['lst_sub_tree']

            new_data.append(item)
            vectors_combined.update(vectors)
            subtrees_combined.extend(subtrees)
    except KeyboardInterrupt:
        update_content(
            processed, new_data,
            subtrees_combined, vectors_combined,
            paths, file_suffix
        )
        exit()

    update_content(
        processed, new_data,
        subtrees_combined, vectors_combined,
        paths, file_suffix
    )


def process_dataset(
    data: List[Dict[str, Any]], skip_ids: List[str], processed: ProcessedData, 
    llm_manager: LLMResponseManager, embed_manager: EmbeddingManager,
    anonymization_key: str, paths: Paths, file_suffix: str,
    main_logger: logging.Logger, num_workers: int, log_file_path: str
) -> None:
    items_to_process = [
        item for item in data
        if item['qid'] not in processed.ids
        and item['qid'] not in skip_ids
    ]

    main_logger.info("remaining items to process: %s", len(items_to_process))

    if num_workers == 1:
        process_dataset_sequential(
            items_to_process, processed,
            llm_manager, embed_manager,
            anonymization_key, paths, file_suffix,
            main_logger
        )
    else:
        process_dataset_parallel(
            items_to_process, processed,
            llm_manager, embed_manager,
            anonymization_key, paths, file_suffix,
            main_logger, num_workers, log_file_path
        )


parser = argparse.ArgumentParser(
    description="Run data creation pipeline: anonymize-embed-extract"
)
parser.add_argument('--split_name', type=str, required=True, help='split name')
parser.add_argument(
    '--split_split_name', type=str, required=True, help='specific split of compositional splits'
)
parser.add_argument('--split_mode', type=str, required=True, help='split mode')
parser.add_argument('--q_decomposer', type=str, required=True, help='question decomposer')
parser.add_argument('--anonymization_key', type=str, default="",
                    help='v1 or v2 ; if None - raw decompositions only')
parser.add_argument('--anonymizer', type=str, default="gpt4_0125",
                    help='llm used for anonymization')
parser.add_argument('--api_type', type=str, default="azure", help='api type ?')
parser.add_argument('--api_endpoint', type=str, default="", help='')
parser.add_argument('--embedder', type=str, default="text_embedding_ada_002",
                    help='model used for embedding')
parser.add_argument('--embed_api_type', type=str, default="azure", help='api type ?')
parser.add_argument('--embed_api_endpoint', type=str, default="", help='')
parser.add_argument('--num_workers', type=int, default=1, help='number of workers to use')
args = parser.parse_args()

split_name = args.split_name
split_split_name = args.split_split_name
split_mode = args.split_mode
q_decomposer = args.q_decomposer
anonymization_key = args.anonymization_key
anonymizer = args.anonymizer
api_type = args.api_type
api_endpoint = args.api_endpoint
embedder = args.embedder
embed_api_type = args.embed_api_type
embed_api_endpoint = args.embed_api_endpoint
num_workers = args.num_workers


DATASET_NAME = "smcalflow"
FILE_SUFFIX = "trying"

llm_manager = LLMResponseManager(
    model_name=anonymizer, api_type=api_type, api_endpoint=api_endpoint
)
embed_manager = EmbeddingManager(
    model_name=embedder, api_type=embed_api_type, api_endpoint=embed_api_endpoint
)

paths, log_file_path = get_file_paths(
    DATASET_NAME,
    (split_name, split_split_name, split_mode),
    anonymization_key,
    anonymizer,
    q_decomposer
)

main_logger = setup_logger(log_file_path)


data = load_json_file(f"{paths.split}.json")
main_logger.info('total data: %s', len(data))

ref_file = f'{paths.split}{FILE_SUFFIX}.json'
if os.path.isfile(ref_file):
    data_processed_so_far = load_json_file(ref_file)
    lst_sub_tree_processed_so_far = load_json_file(
        f"{paths.flat_split}{FILE_SUFFIX}.json"
    )
    query_vectors_processed_so_far = load_pickle_file(
        f"{paths.flat_split_embedding}{FILE_SUFFIX}.pkl"
    )

    data_id_processed_so_far = [item['qid'] for item in data_processed_so_far]
    main_logger.info("\n data already processed: %s", len(data_processed_so_far))
else:
    data_processed_so_far = []
    data_id_processed_so_far = []
    lst_sub_tree_processed_so_far = []
    query_vectors_processed_so_far = {}


processed = ProcessedData(
    data_processed_so_far, data_id_processed_so_far,
    lst_sub_tree_processed_so_far, query_vectors_processed_so_far
)

skip_ids = []

process_dataset(
    data, skip_ids, processed,
    llm_manager, embed_manager,
    anonymization_key, paths, FILE_SUFFIX,
    main_logger, num_workers, log_file_path
)
