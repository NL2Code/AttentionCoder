# 所有实验的启动函数
'''
% attention抽取方法对比
% attention数量对比
% attention类型比较
% attention位置对比(前、中、后)
% attention引入方法（单轮对话、多轮对话）
% starcoder不同自然语言语料占比对方法提升效果的影响，是否存在一定的相关关系
% prompt对结果影响的消融实验
'''

import sys

from APIUse.utils import condition_factory

sys.path.append("/home/liwei/work/")
import os

os.environ['CURL_CA_BUNDLE'] = ''
from APIUse.experiment_execute import experiment_execute

if __name__ == '__main__':
    # 所有实验的条件组合
    condition_list = []
    # 抽取方法
    extract_methods = ["textRank", "singleRank", "topicRank", "multiPartiteRank", "positionRank"]
    # 自然语言类型
    languages = ["English", "Chinese", "Japanese", "French",  "Spanish"]
    # 模板：
    template = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # 对话轮数
    chat_number = 1
    # 模型列表:
    # 如果是对话模型对比的模板应该是18，19
    # 如果是非对话模型对比的模板应该是20， 21
    # todo 这里用来设置线程池中线程的最大数量
    max_workers = 3
    # todo 这里调整实验的模型
    # model_name_list = ["codellamaInstruct-15B", "codellamaInstruct-7B", "WizardCoder-15B", "WizardCoder-7B", "WizardCoder-3B", "WizardCoder-1B"]
    model_name_list = ["WizardCoder-1B"]
    # todo 这些是用来生成每个线程需要的实验参数，统一放到condition_list中，每一个元素代表一个任务参数
    # baseline
    # 使用的分词结果标识
    word_extract = [
        dict(method="textRank", suffix="_9_NP_VP"),
    ]
    condition_factory(condition_list, model_name_list, ["English", "Chinese", "Japanese", "French",  "Spanish"], word_extract, [0], "results/baseline/", chat_number=1, remark="baseline")
    # English
    word_extract = [
        dict(method="textRank", suffix="_9_VP"),
        dict(method="singleRank", suffix="_9_NP_VP"),
        dict(method="singleRank", suffix="_9_NP_VP_edited"),
    ]
    condition_factory(condition_list, model_name_list, ["English"], word_extract, [18, 19], "results/English/", chat_number=1)
    # Chinese
    word_extract = [
        dict(method="textRank", suffix="_9_NP_VP"),
        dict(method="textRank", suffix="_human"),
    ]
    condition_factory(condition_list, model_name_list, ["Chinese"], word_extract, [18, 19], "results/Chinese/", chat_number=1)
    # French
    word_extract = [
        dict(method="singleRank", suffix="_9_NP_VP"),
        dict(method="singleRank", suffix="_9_NP_VP_edited"),
    ]
    condition_factory(condition_list, model_name_list, ["French"], word_extract, [18, 19], "results/French/", chat_number=1)
    # Japanese
    word_extract = [
        dict(method="topicRank", suffix="_9_NP_VP"),
        dict(method="topicRank", suffix="_9_NP_VP_edited"),
    ]
    condition_factory(condition_list, model_name_list, ["Japanese"], word_extract, [18, 19], "results/Japanese/", chat_number=1)
    # Spanish
    word_extract = [
        dict(method="textRank", suffix="_9_NP_VP"),
        dict(method="textRank", suffix="_9_NP_VP_edited"),
    ]
    condition_factory(condition_list, model_name_list, ["Spanish"], word_extract, [18, 19], "results/Spanish/", chat_number=1)
    for item in condition_list:
        print(item)

    experiment_execute(condition_list, max_workers)


