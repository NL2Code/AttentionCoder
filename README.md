# AttentionCoder
Code for the paper "Improving Natural Language Capability of Code Large Language Model"

### Installation
1. python: 3.10
2. pytorch: Select a gpu version based on the cuda version
3. transformers
4. openai: GPT3.5 and GPT4 are required
5. Install the rest as required

### Use steps
1.Install the human - eval, for model generation result assessment, refer to the link https://github.com/openai/human-eval, Make sure to use python 3.7 or later:
```
$ conda create -n codex python=3.10
$ conda activate codex
```
Check out and install this repository:
```
$ git clone https://github.com/openai/human-eval
$ pip install -e human-eval
```
2.Implement the model result acquisition function in APIUse/generate_implements.py according to the needs of the experimental model

3.Set the corresponding model name in main.py and run the main function

4.Analyze the experimental results
* result files is under results/ and can be set in code
* A final summary file result.csv of the experiment results will be generated in the APIUse directory of the project, which mainly contains the conditions of each experiment and the final automated evaluation results

### Directory Introduction (APIUse)
1. result: Used to store the result file after the request model
2. dataset: HumanEval extends benchmarks to other languages
3. word_extract: Attention files obtained by different extraction rank methods

### Main files Introduction
Note: The path is set in sys in the following file and needs to be reset according to the actual location of the code
```python
import sys
sys.path.append("xxx")
```
1. APIUse/generate_implements.py: implements different LLM method functions to obtain results (refer to the model functions already implemented). Adds the corresponding word in get_model_completion to ensure that main.py can be obtained through the specified model string
2. APIUse/experiment_execut.py: The start class of the experiment, which defines the control of different conditions, if no new variables need to be added without modification, the variables involved in the experiment_execute function are described below
    1. model_name_list: LLM model list, the element is the string of the model name, need to implement the corresponding access function in generate_implaments.py, to ensure the same name, refer to the implementation of gpt-3.5-turbo-0613
    2. languages: List of natural languages involved in the experiment, including English, Chinese, French, Spanish and Japanese
    3. word_extract_list: Word segmentation object list. Each dict contains method and suffix. No modification is required
    4. template_id_list: The template involved in the experiment, int array
    5. result_path: indicates the result storage path
    6. chat_number: indicates the number of session rounds. The current number is 1,2
    7. remark: Remark, which is part of the result file
    8. wordNum: Amount of attention
    9. promptId: indicates whether the baseline value is with_attention and 1 indicates without_attention
3. APIUse/main.py: The main function to start the experiment, which needs to set the experimental conditions, and then passed to experiment_execute, so as to start the experiment

### File name rules
1. xxx.jsonl: The direct result obtained by the request model
2. xxx_processed.jsonl: The targetCode result set extracted by analyzing the direct result
3. xxx_processed.jsonl_results.jsonl: targetCode verification result obtained by running the command
4. xxx_prompt.jsonl: Complete prompt when requesting a model

### Tips
1. When adding a model, the corresponding function must be added to APIUse/generate_implements.py to obtain the result of the model
2. You can categorize the results into different folders by calling experiment_execute several times and specifying a different result_path
3. APIUse/command.txt: Stores the command that verifies the accuracy of the result and invots it in the command function in APIUse to generate the result verification for the model, mainly for processing and evaluation,like:
```
python process_humaneval.py --path=results/test/gpt-3.5-turbo-0613_humanEval_Chinese_text_rank__9_NP_VP_template2.jsonl --out_path=results/test/gpt-3.5-turbo-0613_humanEval_Chinese_text_rank__9_NP_VP_template2_processed.jsonl
evaluate_functional_correctness results/test/gpt-3.5-turbo-0613_humanEval_Chinese_text_rank__9_NP_VP_template2_processed.jsonl --problem_file=../dataSet/human-eval-v2-Chinese.jsonl
```

### Reference
```
@misc{li2024attentioncoder,
      title={Improving Natural Language Capability of Code Large Language Model}, 
      author={Wei Li and Daoguang Zan and Bei Guan and Ailun Yu and Xiaolin Chen and Yongji Wang},
      year={2024},
      eprint={2401.14242},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
