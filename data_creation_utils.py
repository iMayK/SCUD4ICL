import time
from collections import OrderedDict
from typing import List, Dict, Any
import logging

from llm_utils_new import LLMResponseManager, EmbeddingManager, get_prompt, pretty_print_prompt
from llm_anonymizer_prompts import (
    SYSTEM_PROMPT, SYSTEM_PROMPT_2, FEW_SHOT_EXAMPLES, FEW_SHOT_EXAMPLES_2
)

MAX_TRIES = 100
MAX_SLEEP = 50


def generate_qid(
    base_qid: str,
    suffix: str
) -> str:
    return f"{base_qid}_{suffix}" if base_qid else str(suffix)


def traverse_all_subtrees(
    decomposition_tree: Dict[str, Any],
    base_qid: str = "root",
    prefix: str = ""
) -> None:
    for suffix, (query, query_content) in enumerate(decomposition_tree.items(), start=1):
        if 'qid' in query_content:
            current_qid = query_content['qid']
        else:
            current_qid = generate_qid(base_qid, suffix)
        decompositions = query_content['decomposition']
        print(f"{prefix}qid: {current_qid}")
        print(f"{prefix}query: {query}\n")

        traverse_all_subtrees(decompositions, base_qid=current_qid, prefix=prefix+"\t")


def get_query_anonymization_w_retry(
    prompt: List[Dict[str, str]],
    llm_manager: LLMResponseManager,
    logger: logging.Logger
) -> str:
    current_sleep = 5
    anonymized_query = ""
    for _ in range(MAX_TRIES):
        try:
            anonymized_query = llm_manager.get_response(prompt)
            break
        except Exception as e:
            anonymized_query = f"ERROR: {e}"
            time.sleep(current_sleep)
            current_sleep = min(current_sleep * 2, MAX_SLEEP)
    else:
        logger.warning("failed after %s attempts", MAX_TRIES)
        logger.warning("error: %s\n", anonymized_query)

    return anonymized_query


def get_query_anonymization(
    query: str,
    anonymization_key: str,
    llm_manager: LLMResponseManager,
    logger: logging.Logger
) -> str:
    logger.debug("Anonymizing query: %s", query)
    if anonymization_key == "v1":
        sys_prompt = SYSTEM_PROMPT
        few_shot_examples = FEW_SHOT_EXAMPLES
    elif anonymization_key == "v2":
        sys_prompt = SYSTEM_PROMPT_2
        few_shot_examples = FEW_SHOT_EXAMPLES_2
    else:
        raise NotImplementedError
    prompt_messages = get_prompt(query, few_shot_examples, sys_prompt)
    pretty_print_prompt(prompt_messages, logger)

    anonymized_query = get_query_anonymization_w_retry(prompt_messages, llm_manager, logger)
    logger.info("\nLLM Response: %s\n", anonymized_query)

    return anonymized_query


def annotate_all_subtrees(
    decomposition_tree: Dict[str, Any],
    base_qid: str,
    anonymization_key: str,
    llm_manager: LLMResponseManager,
    logger: logging.Logger
) -> None:
    logger.debug("Annotating all subtrees")
    for suffix, (query, query_content) in enumerate(decomposition_tree.items(), start=1):
        decompositions = query_content['decomposition']

        current_qid = query_content.pop('qid', '')
        if not current_qid:
            current_qid = generate_qid(base_qid, suffix)

        updated_query_content = OrderedDict()
        updated_query_content['qid'] = current_qid
        updated_query_content['query'] = query
        if anonymization_key:
            anonymized_query = get_query_anonymization(
                query, anonymization_key, llm_manager, logger
            )
            updated_query_content[f"template_{anonymization_key}_{llm_manager.model_name}"] = \
                anonymized_query
        updated_query_content.update(query_content)
        decomposition_tree[query] = updated_query_content

        annotate_all_subtrees(decompositions, current_qid, anonymization_key, llm_manager, logger)


def get_embedding_w_retry(
    item: str,
    embed_manager: EmbeddingManager,
    logger: logging.Logger
):
    current_sleep = 5
    item_embedding = []
    for _ in range(MAX_TRIES):
        try:
            item_embedding = embed_manager.generate_embedding(item)
            break
        except Exception:
            time.sleep(current_sleep)
            current_sleep = min(current_sleep * 2, MAX_SLEEP)
    else:
        logger.warning("failed to get embedding after %s attempts", MAX_TRIES)
    return item_embedding


def embed_all_subtrees(
    decomposition_tree: List[Dict[str, Any]],
    embedding_key: str,
    query_vectors: Dict[str, Any],
    embed_manager: EmbeddingManager,
    logger: logging.Logger
):
    for query, query_content in decomposition_tree.items():
        qid = query_content['qid']
        decompositions = query_content['decomposition']

        query_vector = get_embedding_w_retry(
            query_content[embedding_key] if embedding_key else query,
            embed_manager,
            logger
        )

        query_vectors[qid] = query_vector

        embed_all_subtrees(decompositions, embedding_key, query_vectors, embed_manager, logger)


def extract_all_subtrees(
    decomposition_tree: Dict[str, Any],
    lst_sub_tree: List[Dict[str, Any]]
) -> None:
    for query, query_content in decomposition_tree.items():
        decompositions = query_content['decomposition']

        sub_tree_content = OrderedDict()
        sub_tree_content['qid'] = query_content['qid']
        sub_tree_content['query'] = query
        sub_tree_content.update(query_content)

        lst_sub_tree.append(sub_tree_content)

        extract_all_subtrees(decompositions, lst_sub_tree)
