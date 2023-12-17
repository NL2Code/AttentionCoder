# 针对不同的关键词抽取算法，进行比较，按照default + attention的形式进行比较

'''
  @ Date: 2023/8/10 15:27
  @ Author: liwei
'''
import time

from human_eval.data import write_jsonl, read_problems
import os
import threading
import subprocess

import openai
import json

# 自己的key
# openai.api_key = "sk-81E5lJeL3ow3AB7hCf7400953bB94fF084A80b2e504f4fC7"
from APIUse.process_result import getCommit

openai.api_key = "sk-IwWmK4q8ldllb6lbD0B52cD1935b47589972Ac8241Dd15Fc"
# 目前需要设置代理才可以访问 api
os.environ["HTTP_PROXY"] = "http://localhost:7890/"
os.environ["HTTPS_PROXY"] = "http://localhost:7890/"
model_name = "gpt-3.5-turbo-0613"
# model_name = "gpt-4-0613"
remark = "_without_prefix_without_attention_baseline"
path = "results/baseline/" + model_name + "/"


def get_history_prompt(prompt):
    substring = "\"\"\""
    # 使用 rfind 查找最后一个子串的位置
    last_occurrence = prompt.rfind(substring)

    if last_occurrence != -1:
        # 使用 rfind 查找倒数第二个子串的位置
        second_last_occurrence = prompt[:last_occurrence].rfind(substring)

        if second_last_occurrence != -1:
            return prompt[second_last_occurrence:last_occurrence + 3]
        else:
            return ""
    else:
        return ""

def generate_one_completion(prompt):

    while (True):
        # time.sleep(1)
        try:
            rsp = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    # {"role": "system", "content": "一个有10年Python开发经验的资深算法工程师"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                n=1,
                top_p=0

            )
            return rsp.choices[0].message.content
        except Exception as e:
            print(e)
            print("retrying...")
            continue

    # print(rsp.choices[0].message.content)

def language2problemDataset(langauge):
    if langauge == "Chinese":
        return read_problems("../dataSet/human-eval-v2-Chinese.jsonl")
    elif langauge == "English":
        return read_problems("../dataSet/human-eval-v2-English.jsonl")
    elif langauge == "Japanese":
        return read_problems("../dataSet/human-eval-v2-Japanese.jsonl")
    elif langauge == "French":
        return read_problems("../dataSet/huamn-eval-v2-French.jsonl")
    elif langauge == "German":
        return read_problems("../dataSet/human-eval-v2-German.jsonl")
    elif langauge == "Spanish":
        return read_problems("../dataSet/human-eval-v2-Spanish.jsonl")
    elif langauge == "Russian":
        return read_problems("../dataSet/human-eval-v2-Russian.jsonl")
    else:
       raise Exception("该语言类型不存在")


def get_gpt_results(promptId, language):
    # 遍历方法
    print(promptId, language)
    problems = language2problemDataset(language)
    num_samples_per_task = 1
    samples = [
        dict(task_id=task_id, completion=generate_one_completion(generate_prompt(task_id, problems[task_id]["prompt"], promptId)))
        for task_id in problems
        for _ in range(num_samples_per_task)
    ]
    prompts = [
        dict(task_id=task_id, prompt=generate_prompt(task_id, problems[task_id]["prompt"], promptId))
        for task_id in problems
        for _ in range(num_samples_per_task)
    ]
    write_jsonl(path + model_name + "_humanEval_" + language + "_" + remark + ".jsonl", samples)
    write_jsonl(path + model_name + "_humanEval_" + language + "_" + remark + "_prompt.jsonl", prompts)



# 把关键词放到commit里面
def generate_prompt(task_id, input, promptId):
    print(task_id)
    INSTRUCTION = ""
    # 词性_prefix编号
    if promptId == 0:
        INSTRUCTION = f"""
{input}
"""
    elif promptId == 1:
        # baseline
        INSTRUCTION = f"""
{input}
"""
    if task_id == "HumanEval/0":
        write_jsonl("prompt_remain_" + remark + ".jsonl", [dict(task_id="HumanEval/0", prompt=INSTRUCTION, remark=remark)])
        print(INSTRUCTION)
    return INSTRUCTION



def generate_result_by_multi_prefix(languages, num_threads_list):
    # threads = []
    # for language in languages:
    #     for i in num_threads_list:
    #
    #         thread2 = threading.Thread(target=get_gpt_results, args=(i, language))
    #         threads.append(thread2)
    #         thread2.start()
    #
    # # 等待所有线程执行结束
    # for thread in threads:
    #     thread.join()


    # 执行命令
    for language in languages:
        for i in num_threads_list:
            command = "python process_humaneval.py --path=" + path + model_name + "_humanEval_" + language + "_" + remark + ".jsonl" + " --out_path=" + path + model_name + "_humanEval_" + language + "_" + remark + "_processed.jsonl"
            print(command)
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # 输出命令的标准输出和标准错误import pke
            print("Standard Output:")
            print(result.stdout)
            command2 = "evaluate_functional_correctness " + path + model_name + "_humanEval_" + language + "_" + remark + "_processed.jsonl" + " --problem_file=../dataSet/human-eval-v2-Chinese.jsonl"
            print(command2)

    print('All threads finished.')

if __name__ == '__main__':
    generate_result_by_multi_prefix(["English", "Chinese"], [0])