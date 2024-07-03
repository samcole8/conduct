#!/bin/python3

import sys
import yaml
import os
import subprocess
import shutil

def load_args():
    return sys.argv[1], sys.argv[2]

def get_paths():
    # Get file locations
    source = os.path.abspath(".")
    work_dir = os.path.abspath(os.path.expanduser("~/.conduct"))
    return source, work_dir

def extract_secrets(secrets_file_path):
    # Load secrets into dict
    with open(secrets_file_path, "r") as secrets_file:
        secrets = yaml.safe_load(secrets_file)
    return secrets

def sow(source, work_dir, secrets):
    # Clone directory with secrets
    for root, dirs, files in os.walk(source):
        dest_root = root.replace(source, work_dir, 1)
        if not os.path.exists(dest_root):
            os.makedirs(dest_root)
        for file in files:
            source_file_path = os.path.join(root, file)
            dest_file_path = os.path.join(dest_root, file)
            with open(source_file_path, "r") as source_file, open(dest_file_path, "w") as dest_file:
                for line in source_file:
                    flag_start = line.find("SECRET_")
                    if flag_start >= 0:
                        flag_end = flag_start + 7
                        secret_end = line.find('"' or " ", flag_end)
                        print(secret_end)
                        if secret_end == -1:
                            if "\n" in line:
                                secret_end = len(line) - 1
                            else:
                                secret_end = len(line)
                        key = line[flag_end:secret_end].upper()
                        line = line[:flag_start] + secrets[key] + line[secret_end:]
                    dest_file.write(line)


def execute(work_dir, command):
    # Run docker compose on skeleton dir
    process = subprocess.Popen(command, shell=True, cwd=work_dir)
    process.wait()

    # Clean up
    shutil.rmtree(work_dir)

def run():
    secrets_file_path, command = load_args()
    source, work_dir = get_paths()
    secrets = extract_secrets(secrets_file_path)
    sow(source, work_dir, secrets)
    execute(work_dir, command)

if __name__ == "__main__":
    run()