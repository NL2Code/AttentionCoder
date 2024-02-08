import re

from human_eval.data import read_problems, write_jsonl

from APIUse.generate_implements import get_model_completion
from APIUse.utils import create_message


def get_gpt_extract_result(comment):
    model_name = "gpt-3.5-turbo-0613"
    generate_one_completion = get_model_completion(model_name)
    message = f'''For the following code problem description, extract the key phrases that need to be considered in focus to solve the problem: \n {comment}'''
    # print(message)
    result = generate_one_completion(create_message(message))
    print(result)
    return result


def extract_words_by_gpt():
    languages = ["Japanese", "Spanish", "French"]
    for language in languages:
        comments = read_problems("code_comment_files/result_humaneval_" + language + "_code_comment_.jsonl")
        samples = [
            dict(task_id=task_id, keyWords=get_gpt_extract_result(comments[task_id]["keyWords"]))
            for task_id in comments
            for _ in range(1)
        ]
        write_jsonl("words_extract/result_humaneval_" + language.lower() + "_keywords_by_gpt", samples)


def get_key_words(text):
    text = text + "\n"
    pattern = r'[-]\s?(.*)\n'  # Regular expression pattern that matches the content between "-" (optional) and "("
    matches = re.findall(pattern, text)
    results = []
    for match in matches:
        results.append(match.strip())
    if results == []:
        return text
    ret = ", ".join(results)
    print(ret)
    ret = re.sub(r'\([^,]*\)', '', ret)
    print(ret)
    return ret


if __name__ == '__main__':
    # process
    # generate
    languages = ["Japanese", "Spanish", "French"]
    for language in languages:
        comments = read_problems("words_extract/result_humaneval_" + language.lower() + "_keywords_by_gpt.jsonl")
        samples = [
            dict(task_id=task_id, keyWords=get_key_words(comments[task_id]["keyWords"]))
            for task_id in comments
            for _ in range(1)
        ]
        write_jsonl("words_extract/result_humaneval_" + language.lower() + "_keywords_by_gpt_process.jsonl", samples)
