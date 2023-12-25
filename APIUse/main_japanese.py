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
    # 模型列表
    model_name_list = ["WizardCoder-7B", ""]
    # 使用的分词结果标识
    word_extract = [
        dict(method="topicRank", suffix="_9_NP_VP"),
        dict(method="topicRank", suffix="_9_NP_VP_edited"),
    ]

    # 0: baseline; 18: 添加了attention的优化
    # 如果需要使用多线程，需要在experiment_execute.py的experiment_execute函数中修改flag控制以及时间等待
    experiment_execute(model_name_list, ["Japanese"], word_extract, [0, 18, 19], "results/Japanese/", chat_number=1)
