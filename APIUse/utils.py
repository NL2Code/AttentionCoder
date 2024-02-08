import ast
import csv
import re
import threading

from human_eval.data import read_problems

# Create thread lock
file_lock = threading.Lock()
csv_lock = threading.Lock()

# Word segmentation folder
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
    elif langauge == "Spanish":
        return read_problems("../dataSet/human-eval-v2-Spanish.jsonl")
    else:
        raise Exception("该语言类型不存在")


# Get the key words obtained by the corresponding language and method
def getLanguageAttentionByMethod(language, method, words_extract_suffix):
    return read_problems(
        words_extract_path + "result_humaneval_" + language.lower() + "_keywords_by_" + method + words_extract_suffix + ".jsonl")


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
    for index, keyWord in enumerate(key_words):
        result.append(str(index + 1) + ". " + keyWord)
    return "\n".join(result)


# Write to file function: Support multithreading
def write_to_file(file_name, content):
    global file_lock
    with file_lock:
        with open(file_name, 'a', encoding='utf-8') as file:
            file.write(content + '\n')


def get_pass1(result):
    # Define regular expression patterns
    pattern = r"{'pass@1':\s*([0-9.]+)}"
    match = re.search(pattern, result)

    # Extract matching results
    if match:
        matched_text = match.group(0)
        value = match.group(1)
        return value
    else:
        return result


# A function to write to a CSV file
def write_to_csv(file_name, data):
    global csv_lock
    with csv_lock:
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)


def condition_factory(condition_list, model_name_list, languages, word_extract_list, template_id_list, result_path,
                      chat_number=1, remark="", wordNum=100, promptId=0):
    # Convert all conditions into a list of tuples, with each tuple list representing an experiment parameter that needs to be run
    for model_name in model_name_list:
        for language in languages:
            for word_extract in word_extract_list:
                for template_id in template_id_list:
                    condition_list.append((model_name, language, word_extract, template_id, result_path, chat_number,
                                           remark, wordNum, promptId))


def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def extract_function_calls(code):
    tree = ast.parse(code)

    function_calls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_calls.append(node.name)
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                function_name = node.func.id
                function_calls.append(function_name)

            elif isinstance(node.func, ast.Attribute):
                function_name = node.func.attr
                function_calls.append(function_name)
    function_calls = remove_duplicates(function_calls)
    return ". ".join(function_calls)
