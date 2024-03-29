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

problems = read_problems()


def process_result(completion):
    # 是否含有def
    if "def" in completion:
        return completion
    if completion[:4] != "    ":
        if "\n" in completion:
            index = completion.index("\n")
            if completion[index + 1: index + 5] == "    ":
                return "    " + completion
            else:
                return "    " + completion.replace("\n", "\n    ")
        return "    " + completion.replace("\n", "\n    ")
    else:
        if "\n" in completion:
            index = completion.index("\n")
            if completion[index + 1: index + 5] == "    ":
                return completion
            else:
                return completion.replace("\n", "\n    ")
        else:
            return completion


def exclude_enter(completion):
    pattern = re.compile(r'\n([^ ]+)', re.DOTALL)
    match = pattern.search(completion)
    if match:
        return completion[:match.start()]
    else:
        return completion


output = []
a = 0
for code_file in tqdm(files, total=len(files)):
    codes = [c for c in stream_jsonl(code_file)]
    if args.add_prompt:
        for code in codes:
            flag = False
            task_id = code['task_id']
            # prompt = problems[task_id]['prompt']
            completion2 = code["completion2"]
            if '```python' in completion2 or '``` python' in completion2 or '```' in completion2:
                completion = completion2
            else:
                completion = code["completion1"]

            # completion = code['completion']
            completion = completion.replace("\r", "")
            if '```python' in completion:
                flag = True
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
                flag = True
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
                flag = True
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
                flag = True
                next_line = completion.index('if __name__ == "__main__":')
                completion = completion[:next_line].strip()
                # print(completion)

            if "# Example usage" in completion:
                flag = True
                # print(completion)
                next_line = completion.index('# Example usage')
                completion = completion[:next_line].strip()

            code['completion'] = re.split(r'\n\S', completion.strip())[0]

    output += codes

print("save to {}".format(args.out_path))
write_jsonl(args.out_path, output)
print(a)
