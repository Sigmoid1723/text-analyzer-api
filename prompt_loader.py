import yaml

def load_prompts(filepath="prompts.yaml"):
    with open(filepath,"r") as f:
        return yaml.safe_load(f)
