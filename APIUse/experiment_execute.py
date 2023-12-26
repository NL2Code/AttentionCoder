import sys
# todo 需要根据APIUse在机器上的位置修改一下
sys.path.append("/home/liwei/work/")
import subprocess
import threading
import time
from human_eval.data import write_jsonl, read_problems
import concurrent.futures

from APIUse.generate_implements import get_model_completion
from APIUse.process_result import getCommit
from APIUse.utils import keyWOrds4OrderPrompt, language2problemDataset, getLanguageAttentionByMethod, create_message, \
    wordSelect, write_to_csv, get_pass1, write_to_file


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


# baseline
def generate_prompt0(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
       INSTRUCTION = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{input}\n\n### Response:
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""{input}"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

# 对话模型：attention放置在token中
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
            INSTRUCTION = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{input}\n\n### Response:
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

# 对话模型：attention放置在外部
def generate_prompt19(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            INSTRUCTION = f"""Below is an instruction that describes a task.Pay attention to these below KeyWords in instruction. Write a response that appropriately completes the request.\n\n### Instruction:\n{input}\n\n### KeyWords:\n{attachment}\n\n### Response:
"""

        else:
            INSTRUCTION = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{input}\n\n### Response:
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

# 针对非对话模型
def generate_prompt20(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            _, _, end = getCommit(input)
            input = input[:end] + f"""\n    keywords: {attachment}\n""" + input[end:]
            INSTRUCTION = f"""{input}"""
        else:
            INSTRUCTION = f"""{input}"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""{input}"""
    if task_id == "HumanEval/0":
        print(INSTRUCTION)
    return INSTRUCTION

# 针对非对话模型:attention前添加描述词
def generate_prompt21(task_id, input, attachment, promptId, comment=""):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        if attachment:
            _, _, end = getCommit(input)
            input = input[:end] + f"""\n    Pay attention to these keywords: {attachment}\n""" + input[end:]
            INSTRUCTION = f"""{input}"""
        else:
            INSTRUCTION = f"""{input}"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""{input}"""
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




# word_extract是一个对象：{method:"", suffix: ""}
def get_gpt_results_test(model_name, language, word_extract, template_id, result_path, chat_number, remark="", wordNum=100, promptId=0):
    # 遍历方法
    print("模板对比参数：", model_name,language, word_extract, template_id)

def evaluate_result(model_name, language, word_extract, template_id, result_path, chat_number, remark, wordNum, prompt_id):
    command = "python process_humaneval.py --path=" + result_path + model_name + "_humanEval_" + language + "_" + \
              word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(
        template_id) + ".jsonl" + " --out_path=" + result_path + model_name + "_humanEval_" + language + "_" + \
              word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(
        template_id) + "_processed.jsonl"
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # 输出命令的标准输出和标准错误import pke
    print("Standard Output:")
    print(result.stdout)
    command2 = "evaluate_functional_correctness " + result_path + model_name + "_humanEval_" + language + "_" + \
               word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(
        template_id) + "_processed.jsonl" + " --problem_file=../dataSet/human-eval-v2-" + language + ".jsonl"
    print(command2)
    result2 = subprocess.run(command2, shell=True, capture_output=True, text=True)

    # 将结果写入文件
    write_to_csv("result.csv",
                 [model_name, language, word_extract["method"], word_extract["suffix"], template_id, remark,
                  get_pass1(result2.stdout)])
    print("Standard Output:")
    print(result2.stdout)
    write_to_file("command.txt", command)
    write_to_file("command.txt", command2)

# 指定对比的模板id，以及所需要的分词结果后缀
def experiment_execute(condition_list, max_workers):
    # 线程开始前保证模型参数已经加载
    generate_one_completion = get_model_completion(condition_list[0][0])
    message = generate_one_completion(create_message("测试"))
    if message != "":
        print("model load success!")
    else:
        print("model load wrong!")
        return
    # 线程池完成任务
    # 加载模型参数
    # 定义线程池最大工作线程数
    # 创建 ThreadPoolExecutor 对象，指定线程数为 max_workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 生成结果
        # 提交任务给线程池
        future_to_task = {executor.submit(get_gpt_results, *condition): condition for condition in condition_list}
        # 获取任务执行结果
        for future in concurrent.futures.as_completed(future_to_task):
            condition = future_to_task[future]
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"任务 {condition} 执行出错: {e}")

        # 结果评估
        # 提交任务给线程池
        future_to_task = {executor.submit(evaluate_result, *condition): condition for condition in
                          condition_list}
        # 获取任务执行结果
        for future in concurrent.futures.as_completed(future_to_task):
            condition = future_to_task[future]
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"任务 {condition} 执行出错: {e}")


    # # 代码抽取和结果评估
    # for condition in condition_list:
    #     model_name, language, word_extract, template_id, result_path, chat_number, remark, wordNum, prompt_id = condition
    #     command = "python process_humaneval.py --path=" + result_path + model_name + "_humanEval_" + language + "_" + word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(template_id) + ".jsonl" + " --out_path=" + result_path + model_name + "_humanEval_" + language + "_" + word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(template_id) + "_processed.jsonl"
    #     print(command)
    #     result = subprocess.run(command, shell=True, capture_output=True, text=True)
    #
    #     # 输出命令的标准输出和标准错误import pke
    #     print("Standard Output:")
    #     print(result.stdout)
    #     command2 = "evaluate_functional_correctness " + result_path + model_name + "_humanEval_" + language + "_" + word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(
    #         template_id) + "_processed.jsonl" + " --problem_file=../dataSet/human-eval-v2-" + language + ".jsonl"
    #     print(command2)
    #     result2 = subprocess.run(command2, shell=True, capture_output=True, text=True)
    #
    #     # 将结果写入文件
    #     write_to_csv("result.csv", [model_name, language, word_extract["method"], word_extract["suffix"], template_id, remark, get_pass1(result2.stdout)])
    #     print("Standard Output:")
    #     print(result2.stdout)
    #     # 打开文件以追加模式写入内容，如果文件不存在则创建新文件
    #     with open('command.txt', 'a') as file:
    #         file.write(command + "\n")
    #         file.write(command2 + "\n")

    print(' threads finished.')
# def experiment_execute(model_name_list, languages, word_extract_list, template_id_list, result_path, chat_number=1, remark="", wordNum=100, promptId=0):
#     threads = []
#     # 如果采用的是多线程，需要在第一个线程加载完参数以后（等待一定时间），在执行后续操作
#     flag = False
#     for model_name in model_name_list:
#         for language in languages:
#             for word_extract in word_extract_list:
#                 for template_id in template_id_list:
#                     thread2 = threading.Thread(target=get_gpt_results, args=(model_name, language, word_extract, template_id, result_path, chat_number, remark, wordNum, promptId))
#                     threads.append(thread2)
#                     thread2.start()
#                     if ~flag:
#                        time.sleep(120)
#                        flag = True
#
#     # 等待所有线程执行结束
#     for thread in threads:
#         thread.join()
#
#     # 执行命令
#     for model_name in model_name_list:
#         for language in languages:
#             for word_extract in word_extract_list:
#                 for template_id in template_id_list:
#                     command = "python process_humaneval.py --path=" + result_path + model_name + "_humanEval_" + language + "_" + word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(template_id) + ".jsonl" + " --out_path=" + result_path + model_name + "_humanEval_" + language + "_" + word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(template_id) + "_processed.jsonl"
#                     print(command)
#                     result = subprocess.run(command, shell=True, capture_output=True, text=True)
#
#                     # 输出命令的标准输出和标准错误import pke
#                     print("Standard Output:")
#                     print(result.stdout)
#                     command2 = "evaluate_functional_correctness " + result_path + model_name + "_humanEval_" + language + "_" + word_extract["method"] + "_" + remark + word_extract["suffix"] + "_template" + str(
#                         template_id) + "_processed.jsonl" + " --problem_file=../dataSet/human-eval-v2-" + language + ".jsonl"
#                     print(command2)
#                     result2 = subprocess.run(command2, shell=True, capture_output=True, text=True)
#
#                     # 将结果写入文件
#                     write_to_csv("result.csv", [model_name, language, word_extract["method"], word_extract["suffix"], template_id, remark, get_pass1(result2.stdout)])
#                     print("Standard Output:")
#                     print(result2.stdout)
#                     # 打开文件以追加模式写入内容，如果文件不存在则创建新文件
#                     with open('command.txt', 'a') as file:
#                         file.write(command + "\n")
#                         file.write(command2 + "\n")
#
#     print(' threads finished.')


# if __name__ == '__main__':
    # template_compare_execute()
