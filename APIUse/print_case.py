from human_eval.data import read_problems, write_jsonl

prompt_chinese = read_problems("../dataSet/human-eval-v2-Chinese.jsonl")
result_without_attention = read_problems(
    "results/baseline/gpt-3.5-turbo-0613/gpt-3.5-turbo-0613_humanEval_Chinese__without_prefix_without_attention_baseline_processed.jsonl_results.jsonl")

model_name = "gpt-3.5-turbo-0613"
result_path = "results/methods_compare/gpt-3.5-turbo-0613/"
case_path = "case_study/"
suffix = "template8_method_compare_9_NP_VP"
word_extract_path = "words_extract/"
good_cases = []
bad_cases = []
methods = ["textRank"]
method_suffix = "_9_NP_VP"


def is_Pass(method, task_id):
    result_with_attention = read_problems(
        result_path + model_name + "_humanEval_Chinese_" + method + "__without_prefix_with_attention_" + suffix + "_processed.jsonl_results.jsonl")
    if result_with_attention[task_id]["passed"] is True:
        return True
    else:
        return False


def get_completion(method, task_id):
    result = read_problems(
        result_path + model_name + "_humanEval_Chinese_" + method + "__without_prefix_with_attention_" + suffix + "_processed.jsonl_results.jsonl")
    return result[task_id]


def get_key_words(method, task_id):
    result = read_problems(
        word_extract_path + "result_humaneval_chinese_keywords_by_" + method + method_suffix + ".jsonl")
    return result[task_id]["keyWords"]


for task_id in prompt_chinese:
    success_method = []
    fail_method = []
    good_item = dict()
    bad_item = dict()
    for method in methods:
        if result_without_attention[task_id]["passed"] is not True and is_Pass(method, task_id):
            success_method.append(method)
        if result_without_attention[task_id]["passed"] is True and is_Pass(method, task_id) is not True:
            fail_method.append(method)
    if success_method != []:
        good_item["task_id"] = task_id
        good_item["prompt"] = prompt_chinese[task_id]["prompt"]
        good_item["methods"] = ", ".join(success_method)
        for method in success_method:
            good_item[method] = get_key_words(method, task_id)
        good_cases.append(good_item)
    if fail_method != []:
        bad_item["task_id"] = task_id
        bad_item["prompt"] = prompt_chinese[task_id]["prompt"]
        bad_item["methods"] = ", ".join(fail_method)
        bad_item["test"] = prompt_chinese[task_id]["test"]
        bad_item["originCode"] = result_without_attention[task_id]["completion"]
        for method in fail_method:
            bad_item[method + "Code"] = get_completion(method, task_id)["completion"]
            bad_item[method] = get_key_words(method, task_id)
            bad_item[method + "Error"] = get_completion(method, task_id)["result"]
        bad_cases.append(bad_item)
# df.to_excel('english_solve_problems.xlsx', index=False)
write_jsonl(
    case_path + "good_cases_" + model_name + "_humanEval_Chinese_without_prefix_with_attention_" + suffix + "_processed.jsonl_results.jsonl",
    good_cases)
write_jsonl(
    case_path + "bad_cases_" + model_name + "_humanEval_Chinese_without_prefix_with_attention_" + suffix + "_processed.jsonl_results.jsonl",
    bad_cases)
