#!/bin/python3

import sys
import yaml
import os
import subprocess
import shutil

def load_args():
    return sys.argv[1], sys.argv[2:]

def get_paths():
    # Get file locations
    codebase = os.path.abspath(".")
    work_dir = os.path.abspath(os.path.expanduser("~/.conduct"))
    return codebase, work_dir

def extract_secrets(secrets_file_path):
    # Load secrets into dict
    with open(secrets_file_path, "r") as secrets_file:
        secrets = yaml.safe_load(secrets_file)
    return secrets

def sow(codebase, work_dir, secrets):
    # Clone directory with secrets
    for root, dirs, files in os.walk(codebase):
        dest_root = root.replace(codebase, work_dir, 1)
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
                        secret_end = line.find('"', flag_end)
                        key = line[flag_end:secret_end].upper()
                        line = line[:flag_start] + secrets[key] + line[secret_end:]
                    dest_file.write(line)


def compose(work_dir, docker_args):
    # Run docker compose on skeleton dir
    command = ['docker-compose', '--project-directory', f'"{work_dir}"', 'up'] + docker_args
    command = " ".join(command)
    process = subprocess.Popen(command, shell=True)
    process.wait()

    # Clean up
    shutil.rmtree(work_dir)

def run():
    secrets_file_path, docker_args = load_args()
    codebase, work_dir = get_paths()
    secrets = extract_secrets(secrets_file_path)
    sow(codebase, work_dir, secrets)
    compose(work_dir, docker_args)

if __name__ == "__main__":
    run()