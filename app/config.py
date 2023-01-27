from pathlib import Path

import yaml

CONFIG_FILE = "config.yml"


def read_config():
    config_path = Path(__file__).with_name(CONFIG_FILE)
    return yaml.safe_load(open(config_path, encoding="utf8"))
