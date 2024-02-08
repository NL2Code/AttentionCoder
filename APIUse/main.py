import sys

from APIUse.utils import condition_factory

# todo This needs to be modified based on the location of the APIUse on the machine
sys.path.append("/xxx")
import os

os.environ['CURL_CA_BUNDLE'] = ''
from APIUse.experiment_execute import experiment_execute

if __name__ == '__main__':
    # All experimental conditions are combined
    condition_list = []
    # Extraction method
    extract_methods = ["textRank", "singleRank", "topicRank", "multiPartiteRank", "positionRank"]
    # Natural language type
    languages = ["English", "Chinese", "Japanese", "French", "Spanish"]
    # Template
    template = [0, 1, 2]
    # chat number: one-chat two-chat
    chat_number = 1
    # todo This is used to set the maximum number of threads in the thread pool
    max_workers = 3
    # todo The model of the experiment is adjusted here
    # model_name_list = ["codellamaInstruct-15B", "codellamaInstruct-7B", "WizardCoder-15B", "WizardCoder-7B", "WizardCoder-3B", "WizardCoder-1B"]
    model_name_list = ["codellamaInstruct-7B"]
    # todo These are used to generate condition_list parameters for each thread, each element representing a task parameter

    # example
    # baseline
    # The result identifier of the word segmentation used
    word_extract = [
        dict(method="textRank", suffix="_9_NP_VP"),
    ]
    condition_factory(condition_list, model_name_list, ["English", "Chinese", "Japanese", "French", "Spanish"],
                      word_extract, [0], "results/baseline/", chat_number=1, remark="baseline", promptId=0)
    # English
    word_extract = [
        dict(method="singleRank", suffix="_9_NP_VP"),
    ]
    condition_factory(condition_list, model_name_list, ["English"], word_extract, [1], "results/English/",
                      chat_number=1)
    # Chinese
    word_extract = [
        dict(method="textRank", suffix="_9_NP_VP"),
    ]
    condition_factory(condition_list, model_name_list, ["Chinese"], word_extract, [1], "results/Chinese/",
                      chat_number=1)
    # French
    word_extract = [
        dict(method="singleRank", suffix="_9_NP_VP"),
    ]
    condition_factory(condition_list, model_name_list, ["French"], word_extract, [1], "results/French/",
                      chat_number=1)
    # Japanese
    word_extract = [
        dict(method="topicRank", suffix="_9_NP_VP"),
    ]
    condition_factory(condition_list, model_name_list, ["Japanese"], word_extract, [1], "results/Japanese/",
                      chat_number=1)
    # Spanish
    word_extract = [
        dict(method="textRank", suffix="_9_NP_VP"),
    ]
    condition_factory(condition_list, model_name_list, ["Spanish"], word_extract, [1], "results/Spanish/",
                      chat_number=1)

    for item in condition_list:
        print(item)

    experiment_execute(condition_list, max_workers)
