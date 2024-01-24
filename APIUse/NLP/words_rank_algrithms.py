#coding=utf-8
import spacy

import pke
from human_eval.data import read_problems, write_jsonl

extractorTextRank = pke.unsupervised.TextRank()
extractorMultipartiteRank = pke.unsupervised.MultipartiteRank()
extractorSingleRank = pke.unsupervised.SingleRank()
extractorPositionRank = pke.unsupervised.PositionRank()
extractorTopicRank = pke.unsupervised.TopicRank()

proper_nouns = []
stopwords = []

words_extract_path = "../words_extract/"
pos = {"NOUN", "ADJ", "ADV", "PROPN", "VERB", "DET", "PART", "PRON", "NUM", "ADP", "CONJ"}
# pos = {"NOUN", "PROPN", "VERB"}


def deduplicates_filter(input_list):
    seen = set()
    deduplicated_list = []
    for item in input_list:
        if item not in seen:
            deduplicated_list.append(item)
            seen.add(item)
    result = []
    for word in deduplicated_list:
        result.append(word)
    return result

def language2symbol(language):
    if language == "English":
        return 'en'
    elif language == "Japanese":
        return 'ja'
    elif language == 'German':
        return 'de'
    elif language == 'Chinese':
        return 'zh'
    elif language == 'Spanish':
        return 'es'
    elif language == 'French':
        return 'fr'
    elif language == "Russian":
        return 'ru'
    else:
        return ""

def language2problemDataset(langauge):
    if langauge == "Chinese":
        return read_problems("../../dataSet/human-eval-v2-Chinese.jsonl")
    elif langauge == "English":
        return read_problems("../../dataSet/human-eval-v2-English.jsonl")
    elif langauge == "Japanese":
        return read_problems("../../dataSet/human-eval-v2-Japanese.jsonl")
    elif langauge == "French":
        return read_problems("../../dataSet/human-eval-v2-French.jsonl")
    elif langauge == "German":
        return read_problems("../../dataSet/human-eval-v2-German.jsonl")
    elif langauge == "Spanish":
        return read_problems("../../dataSet/human-eval-v2-Spanish.jsonl")
    elif langauge == "Russian":
        return read_problems("../../dataSet/human-eval-v2-Russian.jsonl")
    else:
       raise Exception("Unrecognized language: " + language)


def TextRank(text, language, condition, nlp2):
    print(1)
    extractorTextRank.load_document(input=text, language=language2symbol(language), normalization='none', stoplist=stopwords, spacy_model=nlp2)
    extractorTextRank.candidate_selection(pos=pos)
    extractorTextRank.candidate_weighting(pos=pos)

    words = extractorTextRank.get_n_best(n=10)
    print(", ".join([word[0] for word in words]))
    res = []

    for word in words:
        if language == "Chinese" or language == "Japanese":
            res.append(word[0].replace(" ", ""))
        else:
            res.append(word[0])
    res = deduplicates_filter(res)
    print("textRank")
    print(", ".join(res))
    return ", ".join(res)

def PositionRank(text, language, condition, nlp2):

    extractorPositionRank.load_document(input=text, language=language2symbol(language), normalization='none', stoplist=stopwords, spacy_model=nlp2)
    extractorPositionRank.candidate_selection(condition)
    extractorPositionRank.grammar_selection(condition)
    extractorPositionRank.candidate_weighting(pos=pos)
    words = extractorPositionRank.get_n_best(n=20)

    res = []
    for word in words:
        if language == "Chinese" or language == "Japanese":
            res.append(word[0].replace(" ", ""))
        else:
            res.append(word[0])
    res = deduplicates_filter(res)
    print("positionRank")
    print(", ".join(res))
    return ", ".join(res)

def SingleRank(text, language, condition, nlp2):

    extractorSingleRank.load_document(input=text, language=language2symbol(language), normalization='none', stoplist=stopwords, spacy_model=nlp2)
    extractorSingleRank.candidate_selection(pos=pos)
    extractorSingleRank.grammar_selection(condition)
    extractorSingleRank.candidate_weighting(pos=pos)
    words = extractorSingleRank.get_n_best(n=20)
    res = []
    for word in words:
        if language == "Chinese" or language == "Japanese":
            res.append(word[0].replace(" ", ""))
        else:
            res.append(word[0])
    res = deduplicates_filter(res)
    print("singleRank")
    print(", ".join(res))
    return ", ".join(res)

def TopicRank(text, language, condition, nlp2):

    extractorTopicRank.load_document(input=text, language=language2symbol(language), normalization='none', stoplist=stopwords, spacy_model=nlp2)
    extractorTopicRank.candidate_selection(pos=pos)
    extractorTopicRank.grammar_selection(condition)
    extractorTopicRank.candidate_weighting()
    words = extractorTopicRank.get_n_best(n=20)
    res = []
    for word in words:
        if language == "Chinese" or language == "Japanese":
            res.append(word[0].replace(" ", ""))
        else:
            res.append(word[0])
    res = deduplicates_filter(res)
    print("topicRank")
    print(", ".join(res))
    return ", ".join(res)

def MultipartiteRank(text, language, condition, nlp2):
    extractorMultipartiteRank.load_document(input=text, language=language2symbol(language), stoplist=stopwords, normalization='none', spacy_model=nlp2)
    extractorMultipartiteRank.candidate_selection(pos=pos)
    extractorMultipartiteRank.grammar_selection(condition)
    extractorMultipartiteRank.candidate_weighting()
    words = extractorMultipartiteRank.get_n_best(n=20)
    res = []
    for word in words:
        if language == "Chinese" or language == "Japanese":
            res.append(word[0].replace(" ", ""))
        else:
            res.append(word[0])
    res = deduplicates_filter(res)
    print("multipartiteRank")
    print(", ".join(res))
    return ", ".join(res)


def language2Model(language):
    if language == "English":
        return "en_core_web_trf"
    elif language == "Chinese":
        return "zh_core_web_trf"
    elif language == "Japanese":
        return "ja_core_news_trf"
    elif language == "Spanish":
        return "es_dep_news_trf"
    elif language == "French":
        return "fr_dep_news_trf"
    else:
        print("Unrecognized language: " + language)
        return ""




if __name__ == '__main__':

    # Example
    text = "John buys twice as many red ties as blue ties.  The red ties cost 50% more than blue ties.  He spent $200 on blue ties that cost $40 each. How much did he spend on ties?"
    language = "English"
    nlp = spacy.load(language2Model(language))
    TextRank(text, "English", "NNP: {<ADJ|DET>*<NOUN|PRON>+}\n" \
            "NP: {<NUM><NNP>*<ADP>*<NNP>*}\n", nlp)

    # Extractor
    languages = ["English"]
    for language in languages:
        print(language2Model(language))
        nlp = spacy.load(language2Model(language))
        # nlp.tokenizer.pkuseg_update_user_dict(proper_nouns)
        print(language)
        dataset = language2problemDataset(language)
        conditions = {
            "VP": "NNP: {(((<NOUN|PROPN|ADJ|DET|NUM><PART>?)|((<VERB><ADV|NUM|ADP|DET|CONJ>*)+<PART>))+<NOUN|PROPN>+) | <NOUN|PROPN><NOUN|PROPN>+ }\n" \
        "NP: {<PRON>*(<ADV>*<VERB>)+<NOUN|PROPN|NNP>}\n" ,
            "NP": "NP: {(((<NOUN|PROPN|ADJ|DET|NUM><PART>?)|((<VERB><ADV|NUM|ADP|DET|CONJ>*)+<PART>))+<NOUN|PROPN>+) | <NOUN|PROPN><NOUN|PROPN>+ }\n" ,
            "NP_VP": "NNP: {(((<NOUN|PROPN|ADJ|DET|NUM><PART>?)|((<VERB><ADV|NUM|ADP|DET|CONJ>*)+<PART>))+<NOUN|PROPN>+) | <NOUN|PROPN><NOUN|PROPN>+ }\n" \
        "VP: {<PRON>*(<ADV>*<VERB>)+<NOUN|PROPN|NNP>}\n" \
        "NP: {<NNP>|<VP>}"
        }
        for key, condition in conditions.items():
            textRank = []
            positionRank = []
            singleRank = []
            topicRank = []
            multiPartiteRank = []
            code_comments = read_problems("../code_comment_files/result_humaneval_" + language + "_code_comment_.jsonl")
            for task_id, _ in enumerate(code_comments):
                # print(task_idask_id)
                # text = getCommit(dataset[task_id]["prompt"])[0]

                text = code_comments[task_id]["keyWords"]
                # text = code_comments[task_id]["question"]
                if language == "Chinese" or language == "Japanese":
                    text = text.replace(" ", "").replace("\n", "")
                textRank.append(dict(task_id=task_id, keyWords=TextRank(text, language, condition, nlp)))
                singleRank.append(dict(task_id=task_id, keyWords=SingleRank(text, language, condition, nlp)))
                positionRank.append(dict(task_id=task_id, keyWords=PositionRank(text, language, condition, nlp)))
                topicRank.append(dict(task_id=task_id, keyWords=TopicRank(text, language, condition, nlp)))
                multiPartiteRank.append(dict(task_id=task_id, keyWords=MultipartiteRank(text, language, condition, nlp)))
            write_jsonl(words_extract_path + "result_humaneval_" + language.lower() + "_keywords_by_textRank_15_" + key + ".jsonl", textRank)
            write_jsonl(words_extract_path + "result_humaneval_" + language.lower() + "_keywords_by_singleRank_9_" + key + ".jsonl", singleRank)
            write_jsonl(words_extract_path + "result_humaneval_" + language.lower() + "_keywords_by_positionRank_9_" + key + ".jsonl", positionRank)
            write_jsonl(words_extract_path + "result_humaneval_" + language.lower() + "_keywords_by_topicRank_9_" + key + ".jsonl", topicRank)
            write_jsonl(words_extract_path + "result_humaneval_" + language.lower() + "_keywords_by_multiPartiteRank_9_" + key + ".jsonl", multiPartiteRank)
