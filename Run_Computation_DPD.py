import os
import csv
from thop import profile, clever_format
import torch
from transformers import AutoModel, AutoTokenizer

device = "cuda" if torch.cuda.is_available() else "cpu"  # Set the device to cuda if available, else use CPU
checkpoint = "./codet5p"  # Path to the directory containing both pytorch_model.bin and config.json

# Load the tokenizer and model using the local path to pytorch_model.bin
tokenizer = AutoTokenizer.from_pretrained(checkpoint, local_files_only=True, trust_remote_code=True)
model = AutoModel.from_pretrained(checkpoint, local_files_only=True, trust_remote_code=True, ignore_mismatched_sizes=True).to(device)

def encode_tokens_codeT5(code):
    inputs = tokenizer.encode(code, return_tensors="pt").to(device)
    return inputs


def flopsparam(input_code):
    flops, params = profile(model, inputs=(encode_tokens_codeT5(input_code),))
    flops, params = clever_format([flops, params], "%.3f")
    return flops, params 

def process_directory(directory_path, output_csv):
    # Use 'a' (append) mode instead of 'w' (write) mode to avoid overwriting the file
    with open(output_csv, 'a', newline='') as csvfile:
        fieldnames = ['File', 'Flops', 'Params']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        flops, params = flopsparam(file_content)

                        writer.writerow({'File': file, 'Flops': flops, 'Params': params})
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")

# Replace 'DPD_Att' with the actual directory path and 'Flops&params.csv' with your desired CSV file name
process_directory(r'C:\Users\ilyes\OneDrive\Bureau\DP_Att\DPD_Att', 'complexity_DPD_att.csv')
