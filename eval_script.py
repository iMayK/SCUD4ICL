print("eval_script.py is being imported")

"""
eval code
"""

import os
import re
import sys
import json
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm

from prompts.dsl_prompts import FULL_DD_WO_DO as SYS_PROMPT_DSL
from prompts.python_prompts import FULL_DD as SYS_PROMPT_PY

from utils import load_json_file, dump_json_file
from data_load_utils import get_complete_configuration

from eval.smcalflow.simplified import evaluate_smcalflow_simplified
from eval.smcalflow.run_program import run_program

# p = "CreateEvent( AND( with_attendee( John ) , with_attendee( FindManager( John ) ) , has_subject( meeting ) , starts_at( Tomorrow( ) ) , starts_at( NumberAM( 8 ) ) ) )"
# g = "do( Let( x0 , John ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindManager( $ x0 ) ) , starts_at( Tomorrow( ) ) , starts_at( NumberAM( 8 ) ) ) ) )"
# print(evaluate_smcalflow_simplified(p, g))

# SYS_PROMPT = FULL_DD_WO_DO


def str_replace(cur_code):
    cur_code = re.sub(r'\\', '', cur_code)
    cur_code = re.sub(r'\"', '', cur_code)
    cur_code = re.sub(r'\'', '', cur_code)
    return cur_code


def process_item(item, pred_key, code_generator, prompt_lang):
    gold_target = item['code']
    pred_target = item[pred_key]
    if prompt_lang != "py_code":
        pred_target = str_replace(pred_target)
    if code_generator == "codegemma:7b":
        pred_target = pred_target.split("<end_of_turn>")[0].strip()

    print(f"\n\ngold: {gold_target}")
    print(f"pred: {pred_target}")

    if prompt_lang == "py_code":
        exec_result = run_program(pred_target)
        if not exec_result["success"]:
            result = {
                "success": False,
                "denotation_accuracy": 0,
                "accuracy": 0,
                "exact_match": 0,
                "execution_error": exec_result["error"]
            }
            item_status = item.setdefault('result', {})
            item_status[pred_key] = {}
            for metric_name, metric_value in result.items():
                item_status[pred_key][metric_name] = metric_value
            item[f"{pred_key}_TO_CODE"] = "FAILED to convert"
            return result
        else:
            pred_target = exec_result["answer"]
            item[f"{pred_key}_TO_CODE"] = pred_target
            print(f"pred (python to dataflow): {pred_target}")

    metrics = evaluate_smcalflow_simplified(pred_target, gold_target)

    item_status = item.setdefault('result', {})
    item_status[pred_key] = {}
    result = {}
    for metric_name, metric_value in metrics.items():
        result[metric_name] = metric_value
        item_status[pred_key][metric_name] = metric_value

    return result


def prepare_and_eval(config_data):
    dataset_name = config_data['dataset_name']
    code_generator = config_data['code_generator']
    prompt_lang = config_data['prompt_lang']
    is_hindi_mode = config_data['is_hindi_mode']

    if is_hindi_mode and prompt_lang == 'py_code':
        raise ValueError("Hindi mode is not supported for python code generation")

    complete_configuration = get_complete_configuration(config_data)
    config_name = complete_configuration["Config Name"]
    input_path = complete_configuration["Input Path"]
    output_path = complete_configuration["Output Path"]

    if not os.path.isfile(input_path):
        print("file is not there, first do the selection")
        # exit()
        return

    a = config_data['SETTING']
    b = config_data.get('candidate_decompositions_name', config_data.get('candidate_name'))
    n = config_data['NUM_ICL']

    if 'candidate_split_mode' in config_data:
        c = config_data['candidate_split_mode']
    else:
        temp = load_json_file(
            f"outputs/smcalflow/{config_data['baseline_path']}.json"
        )['config']
        c = temp['candidate_split_mode']
        a = f"{a}_{temp['SETTING']}"
        n = f"{n}_{temp['NUM_ICL']}"

    d = config_data['test_split_name']
    e = config_data['code_generator']

    log_prefix = f"outputs/{dataset_name}/{e}_{a}_{b}_{c}_{d}_{n}"
    log_file = f"{log_prefix}_eval_log.txt"
    results_file = f"{log_prefix}_eval_results.jsonl"

    data = load_json_file(input_path)
    data_output = data['output']
    config_data = data['config']

    log_file_ptr = open(log_file, 'a')
    results_ptr = open(results_file, 'a')

    if prompt_lang:
        pred_key = f"{code_generator}_{prompt_lang}_w_full_dd"
    else:
        pred_key = f"{code_generator}_wo_full_dd"

    if is_hindi_mode:
        pred_key = f"{pred_key}_hindi"

    # currently setting the pred_key to the latest run
    max_x = 0
    pred_pattern = re.compile(f"{re.escape(pred_key)}_run_(\d+)")
    for key in data_output[0].keys():
        match = pred_pattern.match(key)
        if match:
            x = int(match.group(1))
            max_x = max(max_x, x)
    if max_x > 0:
        pred_key = f"{pred_key}_run_{max_x}"

    ORIGINAL_STDOUT = sys.stdout
    ORIGINAL_STDERR = sys.stderr

    if 'result' in data_output[0] and pred_key in data_output[0]['result'] and 0:
        print('\n\nALREADY COMPUTED, SKIPPING!!!!\n')
        print(f"{json.dumps(config_data[pred_key])}\n\n")
        # results_ptr.write(json.dumps(config_data) + '\n')
        # exit()
        return
    elif pred_key not in data_output[0]:
        print('\n\n\tLLM prediction missing; firse generate the code')
        # exit()
        return
    else:
        print(f"\n\nrunning: {config_name}_[{pred_key}]\n")
        print(f"log_file_path: {log_file}\n\n")
        sys.stdout = log_file_ptr
        sys.stderr = log_file_ptr
        results = []
        for idx, item in tqdm(enumerate(data_output), total=len(data_output)):
            result = process_item(item, pred_key, code_generator, prompt_lang)
            results.append(result)

            new_item = {}
            keys_to_keep_at_last = ['leaves', 'selected_samples']
            for k in item:
                if k not in keys_to_keep_at_last:
                    new_item[k] = item[k]
            for k in keys_to_keep_at_last:
                if k in item:
                    new_item[k] = item[k]

            data_output[idx] = new_item
        sys.stdout = ORIGINAL_STDOUT
        sys.stderr = ORIGINAL_STDERR

        df = pd.DataFrame(results)
        df_dict = df.select_dtypes(include=np.number).mean().to_dict()

        config_data.update({pred_key: df_dict})

        print(f"\n{df_dict}\n\n")

        results_ptr.write(json.dumps(config_data) + '\n')
        dump_json_file(output_path, {'config': config_data, 'output': data_output})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process parameters.")
    parser.add_argument("--config", type=str, help="Path to the configuration file.")
    args = parser.parse_args()

    config_path = args.config

    config_data = load_json_file(config_path)

    prepare_and_eval(config_data)
