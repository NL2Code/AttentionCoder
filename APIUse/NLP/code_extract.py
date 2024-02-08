from human_eval.data import read_problems, write_jsonl

from APIUse.utils import extract_function_calls

if __name__ == '__main__':
    origin_code = "python"
    num_samples_per_task = 1
    origin_prompt = read_problems("../../humaneval-x/" + origin_code + "/data/humaneval_" + origin_code + ".jsonl")
    samples = [
        dict(task_id=task_id, keyWords=extract_function_calls(
            origin_prompt[task_id]["declaration"] + origin_prompt[task_id]["canonical_solution"]))
        for task_id in origin_prompt
        for _ in range(num_samples_per_task)
    ]
    write_jsonl("../words_extract/" + "code_translate_" + origin_code.lower() + "_keywords_function_call.jsonl",
                samples)
