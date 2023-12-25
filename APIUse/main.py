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
sys.path.append("/home/liwei/work/")
import os

os.environ['CURL_CA_BUNDLE'] = ''
from APIUse.experiment_execute import experiment_execute

if __name__ == '__main__':
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
    model_name_list = ["gpt-3.5-turbo-0613"]
    # 使用的分词结果标识
    # baseline
    word_extract = [
        dict(method="textRank", suffix="_9_NP_VP"),
    ]
    experiment_execute(model_name_list, ["English", "Chinese", "Japanese", "French",  "Spanish"], word_extract, [0], "results/baseline/", chat_number=1, remark="baseline")

    # English
    word_extract = [
        dict(method="textRank", suffix="_9_VP"),
        dict(method="singleRank", suffix="_9_NP_VP"),
        dict(method="singleRank", suffix="_9_NP_VP_edited"),
    ]
    # 0: baseline; 18: 添加了attention的优化
    # 如果需要使用多线程，需要在experiment_execute.py的experiment_execute函数中修改flag控制以及时间等待
    experiment_execute(model_name_list, ["English"], word_extract, [18, 19], "results/English/", chat_number=1)

    # Chinese
    word_extract = [
        dict(method="textRank", suffix="_9_NP_VP"),
        dict(method="textRank", suffix="_human"),
    ]
    experiment_execute(model_name_list, ["Chinese"], word_extract, [18, 19], "results/Chinese/", chat_number=1)

    # French
    word_extract = [
        dict(method="singleRank", suffix="_9_NP_VP"),
        dict(method="singleRank", suffix="_9_NP_VP_edited"),
    ]
    experiment_execute(model_name_list, ["French"], word_extract, [18, 19], "results/French/", chat_number=1)

    # Japanese
    word_extract = [
        dict(method="topicRank", suffix="_9_NP_VP"),
        dict(method="topicRank", suffix="_9_NP_VP_edited"),
    ]
    experiment_execute(model_name_list, ["Japanese"], word_extract, [18, 19], "results/Japanese/", chat_number=1)

    # Spanish
    word_extract = [
        dict(method="textRank", suffix="_9_NP_VP"),
        dict(method="textRank", suffix="_9_NP_VP_edited"),
    ]
    experiment_execute(model_name_list, ["Spanish"], word_extract, [18, 19], "results/Spanish/", chat_number=1)


