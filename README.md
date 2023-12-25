# ExperimentForGPU
用于在服务器上跑相关模型的实验

### 安装包要求
1. python：3.10
2. pytorch: 根据cuda版本选择对应的gpu版本
3. transformers
4. openai: GPT3.5，GPT4需要使用
5. 剩余根据运行需要安装即可

### 使用步骤
1. 安装human-eval，用于模型生成结果评估，参考链接https://github.com/openai/human-eval
Make sure to use python 3.7 or later:
```
$ conda create -n codex python=3.10
$ conda activate codex
```
Check out and install this repository:
```
$ git clone https://github.com/openai/human-eval
$ pip install -e human-eval
```
2. 根据实验模型的需要实现APIUse/generate_implements.py中的模型结果获取函数
3. 在main.py中设置对应的模型名称，运行main函数
4. 分析实验结果
    * 过程文件都存在在results下，可以自行设置
    * 在项目的APIUse目录下会生成一个本次实验结果的最终汇总文件 result.csv文件，主要包含每种实验的条件和最终的自动化评测结果

### 目录介绍 (APIUse)
1. result：用于存储请求模型后的结果文件
2. dataset：HumanEval拓展到其他语言上的benchmark
3. word_extract：不同分词方法获取到的attention文件
4. 其余目录无需关注

### 关注的几个文件
注：以下文件中通过sys设置了路径，需要根据代码的实际位置进行重新设置
```python
import sys
sys.path.append("/home/liwei/work/")
```
1. APIUse/generate_implements.py： 实现不同LLM获取结果的方法函数（参考已经实现的模型函数），在get_model_completion添加对应的分词，保证main.py中可以通过指定模型字符串获取
2. APIUse/experiment_execute.py： 实验的启动类，其中定义了对不同条件的控制，如果不需要添加新的变量无需修改，下面对experiment_execute函数中涉及的变量进行说明
    1. model_name_list： LLM模型列表，元素为模型名称的字符串，需要在generate_implaments.py中实现对应的访问函数，保证名称一致，参考gpt-3.5-turbo-0613的实现
    2. languages： 实验涉及的自然语言列表，包括English，Chinese，French，Russian，German，Spanish，Japanese
    3. word_extract_list： 分词对象列表，每个dict包含method和suffix（分词文件名后缀），无需修改
    4. template_id_list：实验涉及的模板， int数组
    5. result_path：结果存储路径
    6. chat_number：对话轮数，目前只有1，2
    7. remark：备注，作为结果文件中的一部分
    8. wordNum：attention数量
    9. promptId：用于控制是否为baseline，0为with_attention，1为without_attention
3. APIUse/main.py：实验开始的主函数，这个里面需要对实验条件进行设置，然后传入experiment_execute中，从而开启实验

### result中的文件名说明
1. xxx.jsonl：请求模型获取的直接结果
2. xxx_processed.jsonl：通过分析直接结果提取到的targetCode结果集
3. xxx_processed.jsonl_results.jsonl：运行command.txt命令得到的targetCode校验结果
4. xxx_prompt.jsonl：请求模型时的完整prompt

### 注意事项
1. 添加模型时APIUse/generate_implements.py中必须要添加相应的函数，用于实现该模型结果的获取
2. 可以通过多次调用experiment_execute，指定不同的result_path，来对结果进行不同文件夹的分类
3. APIUse/command.txt：存储通过校验结果准确率的命令，在APIUse下的命令函进行调用，对模型生成结果校验
