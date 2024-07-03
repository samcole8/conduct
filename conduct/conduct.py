#!/bin/python3

import os
import sys
import yaml

from fork import Fork

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