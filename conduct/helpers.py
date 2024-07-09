import yaml

def extract_yaml(yaml_file_path):
    """Load YAML file into dictionary."""
    with open(yaml_file_path, "r") as yaml_file:
        dictionary = yaml.safe_load(yaml_file)
    return dictionary
