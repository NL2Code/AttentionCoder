import csv
import re
import threading

from human_eval.data import read_problems


# 创建线程锁
file_lock = threading.Lock()
csv_lock = threading.Lock()

# 分词文件夹
words_extract_path = "words_extract/"


def language2problemDataset(langauge):
    if langauge == "Chinese":
        return read_problems("../dataSet/human-eval-v2-Chinese.jsonl")
    elif langauge == "English":
        return read_problems("../dataSet/human-eval-v2-English.jsonl")
    elif langauge == "Japanese":
        return read_problems("../dataSet/human-eval-v2-Japanese.jsonl")
    elif langauge == "French":
        return read_problems("../dataSet/human-eval-v2-French.jsonl")
    elif langauge == "German":
        return read_problems("../dataSet/human-eval-v2-German.jsonl")
    elif langauge == "Spanish":
        return read_problems("../dataSet/human-eval-v2-Spanish.jsonl")
    elif langauge == "Russian":
        return read_problems("../dataSet/human-eval-v2-Russian.jsonl")
    else:
       raise Exception("该语言类型不存在")

# 获取对应语言、对应方法得到的key words
def getLanguageAttentionByMethod(language, method, words_extract_suffix):
    return read_problems(words_extract_path + "result_humaneval_" + language.lower() + "_keywords_by_" + method + words_extract_suffix + ".jsonl")


def wordSelect(attention, num):
    keyWords = attention.split(', ')
    if len(keyWords) > num:
        return ", ".join(keyWords[:num])
    return attention

def spaceDelete(words):
    words2 = words.split(",")
    result = []
    for word in words2:
        result.append(word.replace(" ", ""))
    return ", ".join(result)

def create_message(prompt):
    return [{"role": "user", "content": prompt}]


def keyWOrds4OrderPrompt(attachment):
    key_words = attachment.split(", ")
    result = []
    for index , keyWord in enumerate(key_words):
        result.append(str(index + 1) + ". " + keyWord)
    return "\n".join(result)


# 写入文件的函数：支持多线程
def write_to_file(file_name, content):
    global file_lock
    with file_lock:
        with open(file_name, 'a', encoding='utf-8') as file:
            file.write(content + '\n')


def get_pass1(result):
    # 定义正则表达式模式
    pattern = r"{'pass@1':\s*([0-9.]+)}"

    # 进行匹配
    match = re.search(pattern, result)

    # 提取匹配结果
    if match:
        matched_text = match.group(0)  # 获取整个匹配的字符串
        value = match.group(1)  # 获取括号内匹配的部分
        return value
    else:
        return result


# 写入CSV文件的函数
def write_to_csv(file_name, data):
    global csv_lock
    with csv_lock:
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

