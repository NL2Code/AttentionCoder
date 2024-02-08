import sys

# todo This needs to be modified based on the location of the APIUse on the machine
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
    index2 = prompt.find("    Examples")
    if index2 == -1:
        index2 = prompt.find("    For Example")
        if index2 == -1:
            index2 = prompt.find("    For example")
            if index2 == -1:
                index2 = prompt.find("    for example")
                if index2 == -1:
                    index2 = prompt.find("    Example")
                    if index2 == -1:
                        index2 = prompt.find("    example")
                        if index2 == -1:
                            index2 = prompt.find("    E.g.")
                            if index2 == -1:
                                index2 = prompt.find("    >>>")
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
