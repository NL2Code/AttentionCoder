import sys
sys.path.append("/home/liwei/work/")
import subprocess
import threading
import time
from human_eval.data import write_jsonl, read_problems

from APIUse.generate_implements import get_model_completion
from APIUse.process_result import getCommit
from APIUse.utils import keyWOrds4OrderPrompt, language2problemDataset, getLanguageAttentionByMethod, create_message, \
    wordSelect


def generate_prompt2(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            INSTRUCTION = f"""
# Attention
Pay attention to the key of the problem: {attachment}
When solving the following code problem:
{input}
"""
        else:
            INSTRUCTION = f"""
{input}
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

def generate_prompt3(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            INSTRUCTION = f"""
Pay attention to these key words: {attachment}
When solving the following code problem:
{input}
"""
        else:
            INSTRUCTION = f"""
{input}
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

def generate_prompt4(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            INSTRUCTION = f"""
{input}
#  Attention
Key Words: ** {attachment} **
"""
        else:
            INSTRUCTION = f"""
{input}
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

# 把关键词放到commit里面
def generate_prompt5(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            _, _, end = getCommit(input)
            input = input[:end] + f"""\n
#  Attention
Pay attention to the key of the problem: {attachment}\n
""" + input[end:]
            INSTRUCTION = f"""
{input}
"""
        else:
            INSTRUCTION = f"""
{input}
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

def generate_prompt6(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            INSTRUCTION = f"""
{input}
#  Attention
Pay attention to the key of the problem: {attachment}
"""
        else:
            INSTRUCTION = f"""
{input}
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

def generate_prompt7(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            _, _, end = getCommit(input)
            input = input[:end] + f"""\n
    KeyWords: {attachment}\n
""" + input[end:]
            INSTRUCTION = f"""
{input}
"""
        else:
            INSTRUCTION = f"""
{input}
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

def generate_prompt8(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
       INSTRUCTION = f"""
when create a Python script for problem before, pay attention to these key words: {attachment}
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION


def generate_prompt9(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            INSTRUCTION = f"""
When create a Python script for the below problem:
{input}
pay attention to these key words: 
{attachment}
"""
        else:
            INSTRUCTION = f"""
{input}
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

# 把关键词放到commit里面
def generate_prompt10(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            INSTRUCTION = f"""
When create a Python script for the below problem:
{input}
pay attention to these key phrases: 
{keyWOrds4OrderPrompt(attachment)}
"""
        else:
            INSTRUCTION = f"""
{input}
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

def generate_prompt11(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            INSTRUCTION = f"""
When create a Python script for the below problem, pay attention to the attention: :
# Problem
{input}

# Attention
{attachment}
"""
        else:
            INSTRUCTION = f"""
{input}
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

# 把comment和attention都在第二轮对话中体现
def generate_prompt13(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
       INSTRUCTION = f"""
when create a Python script for problem before, pay attention to these key words in the problem description ({comment}): {attachment} 
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

# baseline
def generate_prompt0(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
       INSTRUCTION = f"""{input}"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""{input}"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

def generate_prompt17(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            _, _, end = getCommit(input)
            input = input[:end] + f"""\n
    pay attention to these KeyWords in Code Description before: {attachment}\n
""" + input[end:]
            INSTRUCTION = f"""
{input}
"""
        else:
            INSTRUCTION = f"""
{input}
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

def generate_prompt18(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            _, _, end = getCommit(input)
            input = input[:end] + f"""\n
    KeyWords: {attachment}\n
""" + input[end:]
            INSTRUCTION = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{input}\n\n### Response:
"""

        else:
            INSTRUCTION = f"""
{input}
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

# 获取不同模板的实现拼接函数
def get_generate_prompt(template_id):
    print("get template" + str(template_id))
    return eval("generate_prompt" + str(template_id))

def generate_question_completion(generate_one_completion, generate_prompt, task_id, input, attachment, promptId, comment=""):
    messaage = [
                    # {"role": "system", "content": "一个有10年Python开发经验的资深算法工程师"},
                    {"role": "user", "content": input}
                ]
    completion1 = generate_one_completion(messaage)
    if attachment:
        messaage.append({"role": "assistant", "content": completion1})
        messaage.append({"role": "user", "content": generate_prompt(task_id, input, attachment, promptId, comment)})
        completion2 = generate_one_completion(messaage)
        # 判断第二次结果中是否存在代码，如果不存在直接使用第一次对话结果
        completion_merge = ""
        if "Yes" in completion2:
            completion_merge = completion1
        else:
            completion_merge = completion2
        return completion1, completion2, completion_merge
    else:
        return completion1, "", completion1

def generate_question_answer_for_dict(generate_one_completion, generate_prompt, task_id, input, attachment, promptId, chat_number=1, comment=""):
    # 生成dict结果
    if chat_number > 1:
        completion1, completion2, completion_merge = generate_question_completion(generate_one_completion, generate_prompt, task_id, input, attachment, promptId, comment)
        return dict(task_id=task_id, completion=completion_merge, completion1=completion1, completion2=completion2)
    else:
        return dict(task_id=task_id, completion=generate_one_completion(create_message(
            generate_prompt(task_id, input, attachment, promptId))))


# word_extract是一个对象：{method:"", suffix: ""}
def get_gpt_results(model_name, language, word_extract, template_id, result_path, chat_number, remark="", wordNum=100, promptId=0):
    # 遍历方法
    print("模板对比参数：", model_name,language, word_extract, template_id)
    problems = language2problemDataset(language)
    comments = read_problems("code_comment_files/result_humaneval_" + language + "_code_comment_.jsonl")
    attentions = getLanguageAttentionByMethod(language, word_extract["method"], word_extract["suffix"])
    num_samples_per_task = 1
    generate_one_completion = get_model_completion(model_name)
    generate_prompt = get_generate_prompt(template_id)
    samples = [
        generate_question_answer_for_dict(generate_one_completion, generate_prompt, task_id, problems[task_id]["prompt"], wordSelect(attentions[task_id]["keyWords"], wordNum), promptId, chat_number)
        for task_id in problems
        for _ in range(num_samples_per_task)
    ]
    prompts = [
        dict(task_id=task_id, prompt=generate_prompt(task_id, problems[task_id]["prompt"], wordSelect(attentions[task_id]["keyWords"], wordNum),promptId))
        for task_id in problems
        for _ in range(num_samples_per_task)
    ]
    write_jsonl(
        result_path + model_name + "_humanEval_" + language + "_" + word_extract["method"]  + "_" + remark + word_extract["suffix"] + "_template" + str(template_id) + ".jsonl",
        samples)
    write_jsonl(
        result_path + model_name + "_humanEval_" + language + "_" + word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(template_id) + "_prompt.jsonl",
        prompts)



# 指定对比的模板id，以及所需要的分词结果后缀
def experiment_execute(model_name_list, languages, word_extract_list, template_id_list, result_path, chat_number=1, remark="", wordNum=100, promptId=0):
    threads = []
    # 如果采用的是多线程，需要在第一个线程加载完参数以后（等待一定时间），在执行后续操作
    # flag = False
    for model_name in model_name_list:
        for language in languages:
            for word_extract in word_extract_list:
                for template_id in template_id_list:
                    thread2 = threading.Thread(target=get_gpt_results, args=(model_name, language, word_extract, template_id, result_path, chat_number, remark, wordNum, promptId))
                    threads.append(thread2)
                    thread2.start()
                    # if ~flag:
                      #  time.sleep(120)
                       # flag = True

    # 等待所有线程执行结束
    for thread in threads:
        thread.join()

    # 执行命令
    for model_name in model_name_list:
        for language in languages:
            for word_extract in word_extract_list:
                for template_id in template_id_list:
                    command = "python process_humaneval.py --path=" + result_path + model_name + "_humanEval_" + language + "_" + word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(template_id) + ".jsonl" + " --out_path=" + result_path + model_name + "_humanEval_" + language + "_" + word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(template_id) + "_processed.jsonl"
                    print(command)
                    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    # 输出命令的标准输出和标准错误import pke
                    print("Standard Output:")
                    print(result.stdout)
                    command2 = "evaluate_functional_correctness " + result_path + model_name + "_humanEval_" + language + "_" + word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(
                        template_id) + "_processed.jsonl" + " --problem_file=../dataSet/human-eval-v2-Chinese.jsonl"
                    print(command2)

                    # 打开文件以追加模式写入内容，如果文件不存在则创建新文件
                    with open('command.txt', 'a') as file:
                        file.write(command + "\n")
                        file.write(command2 + "\n")

    print(' threads finished.')


# if __name__ == '__main__':
    # template_compare_execute()
