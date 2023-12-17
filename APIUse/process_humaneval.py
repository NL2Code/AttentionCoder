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
            if completion[index+1: index+5] == "    ":
                return completion
            else:
                return completion.replace("\n", "\n    ")
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
            completion = code['completion']
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

            if "return" in completion and "def" in completion and ~flag:
                # 查找最后一个return 的后一个换行符号
                next_line = completion.rindex('return')
                substr = completion[next_line:]
                try:
                    next_line2 = substr.index('\n')
                    # try:
                    #     start_line = completion.index('from')
                    # except Exception:
                    start_line = completion.index('def')
                    completion = completion[start_line:next_line + next_line2]
                except ValueError:
                    # try:
                    #     start_line = completion.index('from')
                    # except Exception:
                    start_line = completion.index('def')
                    completion = completion[start_line:]

            code['completion'] = process_result(completion)

    output += codes

print("save to {}".format(args.out_path))
write_jsonl(args.out_path, output)
print(a)
