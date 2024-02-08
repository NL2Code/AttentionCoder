import sys

# todo This needs to be modified based on the location of the APIUse on the machine
sys.path.append("xxx")
import time

from human_eval.data import write_jsonl, read_problems
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import threading
import subprocess
import sys
import openai
import torch
import json

openai.api_key = "xxxxx"

# os.environ["HTTP_PROXY"] = "http://localhost:7890/"
# os.environ["HTTPS_PROXY"] = "http://localhost:7890/"

# todo Different global variables need to be created for different models
wizard_coder_model = None
wizard_coder_tokenizer = None
wizard_coder_generation_config = None

if torch.cuda.is_available():
    device = "cuda"
    print("cuda")
else:
    device = "cpu"
    print("cpu")

try:
    if torch.backends.mps.is_available():
        device = "mps"
except:
    pass


def gpt3_5_generate_one_completion(message):
    # return "test"
    while (True):
        # time.sleep(1)
        try:
            rsp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=message,
                temperature=0,
                n=1,
                top_p=0

            )
            return rsp.choices[0].message.content
        except Exception as e:
            print(e)
            print("retrying...")
            continue


def gpt4_generate_one_completion(message):
    # return "test"
    while (True):
        # time.sleep(1)
        try:
            rsp = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=message,
                temperature=0,
                n=1,
                top_p=0

            )
            return rsp.choices[0].message.content
        except Exception as e:
            print(e)
            print("retrying...")
            continue


def get_model(
        load_8bit: bool = False,
        base_model: str = "bigcode/starcoder",
):
    assert base_model, (
        "Please specify a --base_model, e.g. --base_model='bigcode/starcoder'"
    )
    print(base_model)
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=base_model)
    if device == "cuda":
        model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=base_model,
            load_in_8bit=load_8bit,
            torch_dtype=torch.float16,
            device_map="auto",
            # from_tf=True,
        )
    elif device == "mps":
        model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=base_model,
            device_map={"": device},
            torch_dtype=torch.float16,
        )
    model.config.pad_token_id = tokenizer.pad_token_id

    if not load_8bit:
        print("half")
        model.half()  # seems to fix bugs for some users.

    model.eval()
    if torch.__version__ >= "2" and sys.platform != "win32":
        model = torch.compile(model)

    return tokenizer, model


def code_llama_Instruct_15B_one_completion(message):
    # todo See wizardCoder_7B_generate_one_completion(message) for the implementation
    print("def code_llama_Instruct_15B_one_completion(message):")


def code_llama_Instruct_7B_one_completion(message):
    # See wizardCoder_7B_generate_one_completion(message) for the implementation
    print("def code_llama_Instruct_7B_one_completion(message):")


#
def wizardCoder_15B_generate_one_completion(message):
    # todo See wizardCoder_7B_generate_one_completion(message) for the implementation
    print("def wizardCoder_15B_generate_one_completion(message):")


def wizardCoder_7B_generate_one_completion(message):
    # print(message)
    global wizard_coder_model
    global wizard_coder_tokenizer
    global wizard_coder_generation_config
    if wizard_coder_model == None:
        wizard_coder_tokenizer, wizard_coder_model = get_model(base_model='/xxx/wizardCoder7B')
        wizard_coder_generation_config = GenerationConfig(
            pad_token_id=wizard_coder_tokenizer.pad_token_id,
            do_sample=False,
            temperature=0,
            max_length=2048,
            num_return_sequences=1,
            eos_token_id=wizard_coder_tokenizer.eos_token_id,
            # top_p=0
        )

    # print(f"Loaded bigcode/starcoder.")
    prompt = message[0]["content"].replace('    ', '\t')
    prompt_batch = [prompt]

    encoding = wizard_coder_tokenizer(prompt_batch, return_tensors="pt", truncation=True, max_length=2048).to(device)
    with torch.no_grad():
        gen_tokens = wizard_coder_model.generate(
            **encoding,
            generation_config=wizard_coder_generation_config
        )

    if gen_tokens is not None:
        gen_seqs = wizard_coder_tokenizer.batch_decode(gen_tokens, skip_special_tokens=True)
    else:
        gen_seqs = None

    if gen_seqs is not None:
        gen_seq = gen_seqs[0]
        completion_seq = gen_seq.split("### Response:")[1]
        completion_seq = completion_seq.replace('\t', '    ')
        # print(completion_seq)
        return completion_seq
    return ""


def wizardCoder_3B_generate_one_completion(message):
    # todo See wizardCoder_7B_generate_one_completion(message) for the implementation
    print("def wizardCoder_3B_generate_one_completion(message):")


def wizardCoder_1B_generate_one_completion(message):
    # todo See wizardCoder_7B_generate_one_completion(message) for the implementation
    print("def wizardCoder_1B_generate_one_completion(message):")


#

def get_model_completion(model_name):
    if model_name == "gpt-3.5-turbo-0613":
        print("get gpt-3.5-turbo-0613 model completion")
        return gpt3_5_generate_one_completion
    elif model_name == "gpt-4-0613":
        print("get gpt-4-0613 model completion")
        return gpt4_generate_one_completion
    # Add new branches for different model implementations
    # Your model implementation
    elif model_name == "codellamaInstruct-15B":
        return code_llama_Instruct_15B_one_completion
    elif model_name == "codellamaInstruct-7B":
        return code_llama_Instruct_7B_one_completion
    elif model_name == "WizardCoder-15B":
        return wizardCoder_15B_generate_one_completion
    elif model_name == "WizardCoder-7B":
        return wizardCoder_7B_generate_one_completion
    elif model_name == "WizardCoder-3B":
        return wizardCoder_3B_generate_one_completion
    elif model_name == "WizardCoder-1B":
        return wizardCoder_1B_generate_one_completion
    else:
        print("do not find the required model completion")
        return None
