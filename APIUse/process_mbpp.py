import re

from human_eval.data import read_problems, write_jsonl, stream_jsonl
import glob
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()

# Inputs
parser.add_argument(
    '--path',
    type=str,
    help="")
parser.add_argument(
    '--out_path',
    type=str,
    help="")
parser.add_argument(
    '--add_prompt',
    action='store_true',
    default=True,
    help='')

args = parser.parse_args()

# files = sorted(glob.glob(args.path + '/*.jsonl'))
files = sorted(glob.glob(args.path))
print("{} files in {}".format(len(files), args.path))

problems = read_problems("../dataSet/mbpp-English.jsonl")
# 转化为字符串
problems2 = [c for c in stream_jsonl("../dataSet/mbpp-English.jsonl")]

output = []
a = 0
for code_file in tqdm(files, total=len(files)):
    codes = [c for c in stream_jsonl(code_file)]
    if args.add_prompt:
        for code in codes:
            task_id = code['task_id']
            prompt = problems[task_id]['text']
            completion = code['completion']
            # 获取函数名
            func = problems2[task_id-1]['code']
            funcName = ""
            pattern = r"[\s\S]*def (.*?)\("
            try:
                funcName = re.match(pattern, func).group(1)
                print(funcName)
            except Exception as e:
                print(e)
                # print(func)
                # print("no match")
            if '```python' in completion:
                def_line = completion.index('```python')
                completion = completion[def_line:].strip()
                completion = completion.replace('```python', '')
                # print(completion)
                try:
                    next_line = completion.index('```')
                    completion = completion[:next_line].strip()
                except:
                    a += 1
                    print(completion)
                    print("================\n")
                # print(completion)
            if '``` python' in completion:
                def_line = completion.index('``` python')
                completion = completion[def_line:].strip()
                completion = completion.replace('``` python', '')
                # print(completion)
                try:
                    next_line = completion.index('```')
                    completion = completion[:next_line].strip()
                except:
                    a += 1
                    print(completion)
                    print("================\n")
                # print(completion)
            if '```' in completion:
                def_line = completion.index('```')
                completion = completion[def_line:].strip()
                completion = completion.replace('```', '')
                # print(completion)
                try:
                    next_line = completion.index('```')
                    completion = completion[:next_line].strip()
                except:
                    a += 1
                    print(completion)
                    print("================\n")
                # print(completion)
            if "__name__ == \"__main__\"" in completion:
                next_line = completion.index('if __name__ == "__main__":')
                completion = completion[:next_line].strip()
                # print(completion)

            if "# Example usage" in completion:
                # print(completion)
                next_line = completion.index('# Example usage')
                completion = completion[:next_line].strip()

            if "return" in completion and "def" in completion:
                # 查找最后一个return 的后一个换行符号
                next_line = completion.rindex('return')
                substr = completion[next_line:]
                try:
                    next_line2 = substr.index('\n')
                    start_line = completion.index('def')
                    completion = completion[start_line:next_line + next_line2]
                except ValueError:
                    start_line = completion.index('def')
                    completion = completion[start_line:]
            # 函数名替换，保证调用过程的正确性，防止找不到对应的函数
            if (funcName != ""):
                code['completion'] = re.sub(pattern, "def "+funcName + "(", completion, count=1)
            else:
                code['completion'] = completion
            # code['completion'] = completion

    output += codes

print("save to {}".format(args.out_path))
write_jsonl(args.out_path, output)
print(a)
