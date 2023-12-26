import sys
# todo 需要根据APIUse在机器上的位置修改一下
sys.path.append("/home/daoguang/work/")
from human_eval.data import read_problems, write_jsonl
from pandas import DataFrame


# chinese_result = read_problems("../dataSet/human-eval-v2-English.jsonl")
# prompt = read_problems("../dataSet/human-eval-v2-English.jsonl")
# chinese_result = read_problems("result_commit.jsonl")

def getCommit(prompt):
    re = "\"\"\""
    index = prompt.find(re)
    if index == -1:
        re = "\'\'\'"
        index = prompt.find(re)
    index2 = prompt.find("Examples")
    if index2 == -1:
        index2 = prompt.find("For Example")
        if index2 == -1:
            index2 = prompt.find("For example")
            if index2 == -1:
                index2 = prompt.find("for example")
                if index2 == -1:
                    index2 = prompt.find("Example")
                    if index2 == -1:
                        index2 = prompt.find("example")
                        if index2 == -1:
                            index2 = prompt.find("E.g.")
                            if index2 == -1:
                                index2 = prompt.find(">>>")
                                if index2 == -1:
                                    index2 = prompt.find("例如")
                                    if index2 == -1:
                                        index2 = prompt.find("例子")
                                # if index2 == -1:
                                #     index2 = processedPrompt.find("\n\n")
    endIndex = prompt.rfind(re)
    if index2 == -1:
        end = endIndex
    else:
        end = min(endIndex, index2)
    processedPrompt = prompt[index + 3:end]
    # print(processedPrompt)
    return processedPrompt, index + 3, end


# chinese_result = read_problems("../TranslateDemo-py/TranslateDemo/apidemo/translation_humaneval_" + language + "_from_chinese.jsonl")
#     result = []
#     result2 = []
#     number = 3
#     wordsLength = 3
#     wordType = "NP"
#
#     for task_id in chinese_result:
#         # if chinese_result[task_id]["passed"] == False:
#         result.append(dict(task_id=task_id, keyWords=getTeachWordsThree(getCommit(chinese_result[task_id]["prompt"])[0], language, number, wordsLength, wordType)))
#             # result.append(chinese_result[task_id])
#             # result2.append(prompt[task_id])
#         # chinese_prompt.append(prompt_chinese[task_id]['prompt'])
#         # chinese_code.append(problems_chinese[task_id]['completion'])
#         # english_prompt.append(prompt_english[task_id]['prompt'])
#         # english_code.append(problems_english[task_id]['completion'])
#         # test.append(prompt_english[task_id]['test'])
#     # df = DataFrame({'序号': order, '英文生成的代码 ': chinese_code, '中文生成的代码': english_code, '英文Prompt': english_prompt, '中文Prompt': chinese_prompt, 'test': test})
#     # df.to_excel('english_solve_problems.xlsx', index=False)
#     # write_jsonl("result_humaneval_chinese_keywords_NP.jsonl", result)
#     write_jsonl("result_humaneval_" + language + "_keywords_" + wordType + str(number) + str(wordsLength) + ".jsonl", result)

