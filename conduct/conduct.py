#!/bin/python3

"""Package entrypoint.

This module is responsible for gathering CLI arguments, extracting
secrets from "secrets.yml" files, and creating an instance of the Fork
class, passing the required parameters.

Usage: python3 conduct.py /path/to/secrets.yml "your command here"
"""

import os
import sys
import yaml

from fork import Fork

def get_paths():
    """Return required file paths."""
    # Get absolute current path
    src = os.path.abspath(".")
    # Get absolute path to working directory
    dst = os.path.abspath(os.path.expanduser("~/.conduct"))
    return src, dst

def extract_secrets(secrets_file_path):
    """Load secrets from YAML into dictionary."""
    with open(secrets_file_path, "r") as secrets_file:
        secrets = yaml.safe_load(secrets_file)
    return secrets

def run():
    """Gather CLI arguments, get secrets, and pass to Fork instance."""
    secrets_path, command = sys.argv[1], sys.argv[2]
    secrets = extract_secrets(secrets_path)
    src, dst = get_paths()
    # Execute command in forked repository
    with Fork(src, dst, secrets) as fork:
        fork.execute(command)

if __name__ == "__main__":
    run()