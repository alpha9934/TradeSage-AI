import yaml
import os
from pathlib import Path

def load_config(config_path: str = None) -> dict:
    if config_path is None:
        # Get the path of the directory where this file (config_loader.py) is
        current_dir = Path(__file__).parent 
        # Move up one level to the root, then into the config folder
        config_path = current_dir.parent / "config" / "config.yaml"
    
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config