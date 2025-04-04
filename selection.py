import os
from tqdm import tqdm
from joblib import Parallel, delayed
import torch

from utils import load_json_file, dump_json_file, reset_logging, load_pickle_file, dump_pickle_file
from qd_train import setup_logger
from step_by_step_gen_utils import get_id_query_map, prepare_leaves_cache
from selection_methods.cover_source_dd import (
    CoverSource,
    CoverSourceMod, CoverSourceMod2, CoverSourceMod3,
    CoverSourceMod4, CoverSourceMod41,
    CoverSourceMod5, CoverSourceMod51
)
from retrievers.bm25_dd import BM25Retriever
from leaf_only_testset_sel_utils import select_instances

TASK_NAME = "ALL-TESTSET"


def create_similarity_dict(leaf, scores, candidate_keys):
    return leaf, {candidate_keys[i]: score for i, score in enumerate(scores)}


def precompute_similarities(cand_prefix, split_mode, test_name, base_path,
                            batch_size=50, use_gpu=True, n_jobs=16):

    if split_mode.startswith('top-5'):
        split_mode = 'top-5-subset'
    elif split_mode.startswith('top-10'):
        split_mode = 'top-10-subset'

    cand_name = cand_prefix.format(split_mode)

    sim_file_name = f"{base_path}/sim_CAND-{cand_name}_TEST-{test_name}.pkl"
    if os.path.isfile(sim_file_name):
        sim_cache = load_pickle_file(sim_file_name)
        return sim_cache
    else:
        cand_path = f"{base_path}/flat_{cand_name}_vectors.pkl"
        test_path = f"{base_path}/flat_{test_name}_vectors.pkl"
        candidate_vectors = load_pickle_file(cand_path)
        test_vectors = load_pickle_file(test_path)

        device = torch.device('cuda' if torch.cuda.is_available() and use_gpu else 'cpu')

        test_vectors_selected = torch.stack(list(test_vectors.values())).to(device)  # m x d
        candidate_vectors_selected = torch.stack(list(candidate_vectors.values())).to(device)  # n x d

        print('computing cosine similarity')
        num_test_vectors = test_vectors_selected.size(0)
        num_candidate_vectors = candidate_vectors_selected.size(0)

        sim_cache = {}
        test_leaves = list(test_vectors.keys())
        candidate_keys = list(candidate_vectors.keys())
        combined_similarity_scores_list = []

        for start in range(0, num_test_vectors, batch_size):
            end = min(start + batch_size, num_test_vectors)
            batch_test_vectors = test_vectors_selected[start:end]

            similarity_scores = torch.cosine_similarity(
                candidate_vectors_selected.unsqueeze(0),
                batch_test_vectors.unsqueeze(1),
                dim=2
            )
            similarity_scores_list = similarity_scores.cpu().tolist()  # Move back to CPU for further processing
            combined_similarity_scores_list.extend(similarity_scores_list)

        sim_cache = dict(Parallel(n_jobs=n_jobs)(
            delayed(create_similarity_dict)(leaf, scores, candidate_keys)
            for leaf, scores in zip(test_leaves, combined_similarity_scores_list)
        ))

        dump_pickle_file(sim_file_name, sim_cache)
        return sim_cache


def run(**kwargs):
    random_seed = kwargs['random_seed']
    dd_target = kwargs['dd_target']
    base_path = kwargs['base_path']
    cand_prefix = kwargs['cand_prefix']
    test_prefix = kwargs['test_prefix']
    split_mode = kwargs['split_mode']
    K = kwargs['K']
    cover_mode = kwargs['cover_mode']
    is_dd_modified = kwargs['is_dd_modified']
    q_decomposer = kwargs['q_decomposer']
    threshold = kwargs['threshold']
    query_type = kwargs['query_type']
    root_orig_query = kwargs['root_orig_query']
    mistral_mode = kwargs['mistral_mode']
    theta = kwargs['theta']
    amlpp = kwargs['amlpp']

    common_suffix = (
        f"{TASK_NAME}_"
        f"{q_decomposer}{cand_prefix.format(split_mode)}_"
        f"[{test_prefix}]_"
        f"{cover_mode.upper()}"
        f"_K-{K}"
        + ("_freeform_query" if query_type == "query_freeform" else "")
        + ("_root_orig_query" if root_orig_query else "")
        + ("_mistral_mode" if mistral_mode else "")
        + (f"_weightedBM25-theta-{theta}" if theta else "")
        + ("_aml_prime_prime" if amlpp else "")
    )
    if is_dd_modified:
        common_suffix += f"_DD-MOD-v{is_dd_modified}"
    if is_dd_modified in {4, 41, 5, 51}:
        common_suffix += f"_TH-{threshold}"

    output_base_path = f"outputs/smcalflow/{TASK_NAME}"
    output_path = f"{output_base_path}/{common_suffix}.json"

    if os.path.isfile(output_path):
        return

    log_file_name = f"{output_base_path}/../LOGS/{TASK_NAME}/{common_suffix}"
    main_logger = setup_logger(log_file_name)

    input_data = load_json_file(f"{base_path}/{test_prefix}.json")
    root_candidates = load_json_file(f"{base_path}/{q_decomposer}{cand_prefix.format(split_mode)}.json")
    if mistral_mode:
        all_candidates = load_json_file("data/smcalflow/decomposed/mixtral-t5_filtered_gpt4-t5-4pd.json")
    else:
        all_candidates = load_json_file(f"{base_path}/{q_decomposer}flat_{cand_prefix.format(split_mode)}.json")
    flat_tests = load_json_file(f"{base_path}/{q_decomposer}flat_{test_prefix}.json")

    input_data = {
        f"{item['qid']}_1": {**item, 'qid': f"{item['qid']}_1"}
        for item in input_data
    }
    test_ids = list(input_data.keys())

    root_candidates = {
        f"{item['qid']}_1": {**item, 'qid': f"{item['qid']}_1"}
        for item in root_candidates
    }
    all_candidates = {
        item['qid']: {
            "qid": item['qid'],
            "query": root_candidates[item['qid']]['query'] if root_orig_query and len(item['qid'].split('_')) == 2 else
            (item[query_type] if len(item['qid'].split('_')) != 2 else item['query']),
            "code": item['code'],
            dd_target: item[dd_target],
            "decomposition": item['decomposition']
        }
        for item in all_candidates
    }
    flat_tests = {item['qid']: item for item in flat_tests}

    cand_id_to_query, cand_query_to_id = get_id_query_map(all_candidates)
    cand_leaves_cache = {}
    prepare_leaves_cache(all_candidates, cand_id_to_query, cand_leaves_cache)

    test_id_to_query, test_query_to_id = get_id_query_map(flat_tests)
    test_leaves_cache = {}
    prepare_leaves_cache(flat_tests, test_id_to_query, test_leaves_cache)

    leaf_candidates = {}
    for candid in root_candidates:
        leaves = cand_leaves_cache[candid]
        for leaf in leaves:
            leaf_candidates[leaf] = all_candidates[leaf]

    leaf_parent_ids = list(set([leaf.rsplit('_', maxsplit=1)[0] for leaf in leaf_candidates]))
    # remove those parent ids which are root itself
    leaf_parent_ids = [leafp for leafp in leaf_parent_ids if leafp not in root_candidates]
    leaf_parents = {}
    for leaf_p in leaf_parent_ids:
        leaf_parents[leaf_p] = all_candidates[leaf_p]

    all_minus_leaf = {}
    for qid in all_candidates:
        if qid not in leaf_candidates:
            all_minus_leaf[qid] = all_candidates[qid]

    if amlpp:
        for qid in leaf_parents:
            if qid in all_minus_leaf:
                all_minus_leaf.pop(qid)

    for qid in root_candidates:
        root_candidates[qid][dd_target] = all_candidates[qid][dd_target]

    middle_candidates = {}
    for qid in all_candidates:
        if qid not in root_candidates and qid not in leaf_candidates:
            middle_candidates[qid] = all_candidates[qid]

    mid_minus_leafp_candidates = {}
    for qid in middle_candidates:
        if qid not in leaf_parents:
            mid_minus_leafp_candidates[qid] = middle_candidates[qid]

    main_logger.info("leaf candidates %d", len(leaf_candidates))
    main_logger.info("leaf parents %d", len(leaf_parents))
    main_logger.info("middle candidates %d", len(middle_candidates))
    main_logger.info("middle minus leaf parent candidates %d", len(mid_minus_leafp_candidates))
    main_logger.info("root candidates %d", len(root_candidates))
    main_logger.info("all candidates %d", len(all_candidates))
    main_logger.info("all minus leaf candidates %d", len(all_minus_leaf))

    main_logger.info(
        "cand_id_to_query %d, cand_query_to_id %d, cand_leaves_to_cache %d",
        len(cand_id_to_query), len(cand_query_to_id), len(cand_leaves_cache)
    )

    def get_cover_fun(candidates, dd_target, K, is_dd_modified, random_seed, theta, sim_cache=None):
        ret_fun = BM25Retriever(candidates, random_seed)
        if is_dd_modified == 0:
            cover_fun = CoverSource(candidates, random_seed, ret_fun, K, field_for_target=dd_target)
        elif is_dd_modified == 3:
            cover_fun = CoverSourceMod3(candidates, random_seed, ret_fun, K, field_for_target=dd_target, theta=theta)
        else:
            raise ValueError("invalid value for `is_dd_modified`")
        return cover_fun

    if cover_mode == "root":
        candidates = list(root_candidates.values())
    elif cover_mode == "all_minus_leaf":
        candidates = list(all_minus_leaf.values())
    else:
        raise ValueError(f"Invalid cover_mode: {cover_mode}")

    if is_dd_modified in {4, 41, 5, 51}:
        sim_cache = precompute_similarities(cand_prefix, split_mode, test_prefix, base_path)
    else:
        sim_cache = None
    cover_fun = get_cover_fun(candidates, dd_target, K, is_dd_modified, random_seed, sim_cache)

    print(f'running: {common_suffix}')
    main_logger.info('running: %s', common_suffix)

    output_data = []
    for test_id in tqdm(test_ids):
        test_item = input_data[test_id]
        select_instances(test_item, cover_fun, main_logger)
        test_item.pop('decomposition')
        output_data.append(test_item)

    dump_json_file(output_path, output_data)


def main():
    random_seed = 0
    dd_target = "code_anonymized_v2"

    base_path = "data/smcalflow/decomposed"
    cand_prefix = "source_domain_with_target_num0_train_{}"

    test_prefix = "iid_test_PRED"
    # test_prefix = "source_domain_with_target_num0_test_PRED"

    Q_DECOMPOSER = ""                             # for gpt4
    # Q_DECOMPOSER = "mixtral:8x22b" + "_"            # for mixtral:8x22b

    QUERY_TYPE = "query"
    # QUERY_TYPE = "query_freeform"

    THRESHOLD = 0.8     # for versions : 4, 41, 5, 51

    ROOT_ORIG_QUERY = 1

    MISTRAL_MODE = 0

    THETA = 0          # weighted BM25

    AMLPP = 0           # this is to remove leaf parents from `all-leaf` # for rebuttal random expt

    NUM_ICLS = [
        5,
        # 10,
        # 3,
        # 20,
        # 30,
        # 9
    ]
    COVER_MODES = [
        "root",
        "all_minus_leaf",
        # "leaf",
        # "all",
        # "mid",
        # "mid_plus_leaf",
        # "leaf_parents",
        # "mid_minus_leafp",
    ]
    SPLIT_MODES = [
        "random-100-split-4plus-depth",
        # "random-split-4plus-depth",
        # "top-10-subset-4plus-depth",
        # "top-5-subset-4plus-depth",
        # "top-10-subset-5plus-depth",
        # "top-5-subset-5plus-depth",
        # "top-5-subset-3plus-depth",
        # "top-5-subset",
        # "all-python-programs",
        # "top-5-subset-PyV1",
        # "top-10-subset"
    ]
    for K in tqdm(NUM_ICLS):
        for split_mode in tqdm(SPLIT_MODES, leave=False):
            for cover_mode in tqdm(COVER_MODES, leave=False):
                if cover_mode == "root":
                    is_dd_modified = 0
                elif cover_mode == "all_minus_leaf":
                    is_dd_modified = 3

                run(
                    random_seed=random_seed,
                    dd_target=dd_target,
                    base_path=base_path,
                    cand_prefix=cand_prefix,
                    test_prefix=test_prefix,
                    split_mode=split_mode,
                    K=K,
                    cover_mode=cover_mode,
                    is_dd_modified=is_dd_modified,
                    q_decomposer=Q_DECOMPOSER,
                    threshold=THRESHOLD,
                    query_type=QUERY_TYPE,
                    root_orig_query=ROOT_ORIG_QUERY,
                    mistral_mode=MISTRAL_MODE,
                    theta=THETA,
                    amlpp=AMLPP
                )
                reset_logging()


if __name__ == "__main__":
    main()
