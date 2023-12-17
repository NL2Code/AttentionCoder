from human_eval.data import read_problems

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
        return read_problems("../dataSet/huamn-eval-v2-French.jsonl")
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
