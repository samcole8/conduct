#!/bin/python3

import os
import shutil
import subprocess
import sys
import yaml

FLAG = "SECRET_"

class Fork:

    def __init__(self, src, dst, secrets):
        self.src = src
        self.dst = dst
        self.secrets = secrets

    def __enter__(self):
        def embed_secret(line):
            # Get position of secret
            flag_start = line.find(FLAG)
            if flag_start != -1:
                # Get secret start index
                secret_start = flag_start + 7
                secret_end = line.find('"', secret_start)
                # Get secret end index
                if secret_end == -1:
                    if "\n" in line:
                        secret_end = len(line) - 1
                    else:
                        secret_end = len(line)
                # Get key from secret
                key = line[secret_start:secret_end].upper()
                # Construct new line
                line = f"{line[:flag_start]}{self.secrets[key]}{line[secret_end:]}"
            return line

        # Fork directories
        for src_root, dirs, files in os.walk(self.src):
            dst_root = src_root.replace(self.src, self.dst, 1)
            if not os.path.exists(dst_root):
                os.makedirs(dst_root)
            # Fork files
            for file in files:
                src_file_path = os.path.join(src_root, file)
                dst_file_path = os.path.join(dst_root, file)
                with open(src_file_path, "r") as src_file, open(dst_file_path, "w") as dst_file:
                    # Embed secrets
                    for line in src_file:
                        dst_file.write(embed_secret(line))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.dst)
    
    def execute(self, command):
        # Execute command
        process = subprocess.Popen(command, shell=True, cwd=self.dst)
        process.wait()

def get_paths():
    # Get file locations
    src = os.path.abspath(".")
    dst = os.path.abspath(os.path.expanduser("~/.conduct"))
    return src, dst

def extract_secrets(secrets_file_path):
    # Load secrets into dict
    with open(secrets_file_path, "r") as secrets_file:
        secrets = yaml.safe_load(secrets_file)
    return secrets

def run():
    secrets_path, command = sys.argv[1], sys.argv[2]
    secrets = extract_secrets(secrets_path)
    src, dst = get_paths()
    with Fork(src, dst, secrets) as fork:
        fork.execute(command)

if __name__ == "__main__":
    run()