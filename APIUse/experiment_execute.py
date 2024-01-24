import sys
# todo This needs to be modified based on the location of the APIUse on the machine
sys.path.append("xxx")
import subprocess

from human_eval.data import write_jsonl, read_problems
import concurrent.futures

from APIUse.generate_implements import get_model_completion
from APIUse.process_result import getCommit
from APIUse.utils import keyWOrds4OrderPrompt, language2problemDataset, getLanguageAttentionByMethod, create_message, \
    wordSelect, write_to_csv, get_pass1, write_to_file

# baseline
def generate_prompt0(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    if promptId == 0:
       INSTRUCTION = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n\n### Instruction:\nCreate a Python script for this problem:\n{input}\n\n### Response:"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""{input}"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

# one-chat style
def generate_prompt1(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    if promptId == 0:
        if attachment:
            _, _, end = getCommit(input)
            input = input[:end] + f"""\n
    KeyWords: {attachment}\n
""" + input[end:]
            INSTRUCTION = f"""Below is an instruction that describes a task, Write a response that appropriately completes the request.\n\n\n### Instruction:\nCreate a Python script for this problem:\n{input}\n\n### Response:"""

        else:
            INSTRUCTION = f"""Below is an instruction that describes a task, Write a response that appropriately completes the request.\n\n\n### Instruction:\nCreate a Python script for this problem:\n{input}\n\n### Response:"""

    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

# two-chat style
def generate_prompt2(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    if promptId == 0:
       INSTRUCTION = f"""
1. Check out if the target code generated before is correct to match the Code Description
2. If not, pay attention to these KeyWords in Code Description and rewrite the code to be correct
### KeyWords
{attachment}
### Code Description
{comment}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

# Gets implementation concatenation functions for different templates
def get_generate_prompt(template_id):
    print("get template" + str(template_id))
    return eval("generate_prompt" + str(template_id))

def generate_question_completion(generate_one_completion, generate_prompt, task_id, input, attachment, promptId, comment=""):
    first_prompt = input
    messaage = [
                    {"role": "user", "content": first_prompt}
                ]
    completion1 = generate_one_completion(messaage)
    if attachment:
        messaage.append({"role": "assistant", "content": completion1})
        messaage.append({"role": "user", "content": generate_prompt(task_id, input, attachment, promptId, comment)})
        completion2 = generate_one_completion(messaage)
        # Determine if there is code in the second result, and if there is no code, use the first result directly
        completion_merge = ""
        if "```python" not in completion2 and "``` python" not in completion2:
            completion_merge = completion1
        else:
            completion_merge = completion2
        return completion1, completion2, completion_merge
    else:
        return completion1, "", completion1, first_prompt

def generate_question_answer_for_dict(generate_one_completion, generate_prompt, task_id, input, attachment, promptId, chat_number=1, comment=""):
    if chat_number > 1:
        completion1, completion2, completion_merge, first_prompt = generate_question_completion(generate_one_completion, generate_prompt, task_id, input, attachment, promptId, comment)
        return dict(task_id=task_id, completion=completion_merge, completion1=completion1, completion2=completion2, first_prompt=first_prompt)
    else:
        return dict(task_id=task_id, completion=generate_one_completion(create_message(
            generate_prompt(task_id, input, attachment, promptId, comment))))


# word_extract is an object：{method:"", suffix: ""}
def get_gpt_results(model_name, language, word_extract, template_id, result_path, chat_number, remark="", wordNum=100, promptId=0):
    print("Experimental condition：", model_name, language, word_extract, template_id)
    problems = language2problemDataset(language)
    comments = read_problems("code_comment_files/result_humaneval_" + language + "_code_comment_.jsonl")
    attentions = getLanguageAttentionByMethod(language, word_extract["method"], word_extract["suffix"])
    num_samples_per_task = 1
    generate_one_completion = get_model_completion(model_name)
    generate_prompt = get_generate_prompt(template_id)
    samples = [
        generate_question_answer_for_dict(generate_one_completion, generate_prompt, task_id, problems[task_id]["prompt"], wordSelect(attentions[task_id]["keyWords"], wordNum), promptId, chat_number, comment=comments[task_id]["keyWords"])
        for task_id in problems
        for _ in range(num_samples_per_task)
    ]
    prompts = [
        dict(task_id=task_id, prompt=generate_prompt(task_id, problems[task_id]["prompt"], wordSelect(attentions[task_id]["keyWords"], wordNum),promptId, comment=comments[task_id]["keyWords"]))
        for task_id in problems
        for _ in range(num_samples_per_task)
    ]
    write_jsonl(
        result_path + model_name + "_humanEval_" + language + "_" + word_extract["method"]  + "_" + remark + word_extract["suffix"] + "_template" + str(template_id) + ".jsonl",
        samples)
    write_jsonl(
        result_path + model_name + "_humanEval_" + language + "_" + word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(template_id) + "_prompt.jsonl",
        prompts)


def evaluate_result(model_name, language, word_extract, template_id, result_path, chat_number, remark, wordNum, prompt_id):
    command = "python process_humaneval.py --path=" + result_path + model_name + "_humanEval_" + language + "_" + \
              word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(
        template_id) + ".jsonl" + " --out_path=" + result_path + model_name + "_humanEval_" + language + "_" + \
              word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(
        template_id) + "_processed.jsonl"
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Output the standard output and standard error of the command
    print("Standard Output:")
    print(result.stdout)
    command2 = "evaluate_functional_correctness " + result_path + model_name + "_humanEval_" + language + "_" + \
               word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(
        template_id) + "_processed.jsonl" + " --problem_file=../dataSet/human-eval-v2-" + language + ".jsonl"
    print(command2)
    result2 = subprocess.run(command2, shell=True, capture_output=True, text=True)

    # Write the result to a file
    write_to_csv("result.csv",
                 [model_name, language, word_extract["method"], word_extract["suffix"], template_id, remark,
                  get_pass1(result2.stdout)])
    print("Standard Output:")
    print(result2.stdout)
    write_to_file("command.txt", command)
    write_to_file("command.txt", command2)


def experiment_execute(condition_list, max_workers):
    # Ensure that the model parameters are loaded before the thread starts
    generate_one_completion = get_model_completion(condition_list[0][0])
    message = generate_one_completion(create_message("test"))
    if message != "":
        print("model load success!")
    else:
        print("model load wrong!")
        return
    # Thread pool completes the task
    # Load model parameters
    # Define the maximum number of worker threads in the thread pool
    # Create a ThreadPoolExecutor object with max_workers as the number of threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Generate results
        # Submit task to thread pool
        future_to_task = {executor.submit(get_gpt_results, *condition): condition for condition in condition_list}
        # Obtain the task execution result
        for future in concurrent.futures.as_completed(future_to_task):
            condition = future_to_task[future]
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"task {condition} execution error: {e}")

        # Result evaluation
        # Submit task to thread pool
        future_to_task = {executor.submit(evaluate_result, *condition): condition for condition in
                          condition_list}
        # Obtain the task execution result
        for future in concurrent.futures.as_completed(future_to_task):
            condition = future_to_task[future]
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"task {condition} execution error: {e}")

    print(' threads finished.')

