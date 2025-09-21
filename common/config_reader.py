import yaml
from pathlib import Path

class ConfigReader:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config =self._load_config()

    def _load_config(self):
        with open(Path(self.config_path), "r") as f:
            return yaml.safe_load(f)