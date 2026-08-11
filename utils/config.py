"""Configuration utilities for KurupDevs."""
import os
import json
from pathlib import Path
from typing import Any, Optional

CONFIG_DIR = Path("config")
CONFIG_DIR.mkdir(exist_ok=True)


def get_config(key: str, default: Any = None) -> Any:
    """Get a configuration value."""
    config_file = CONFIG_DIR / "settings.json"
    if not config_file.exists():
        return default
    try:
        with open(config_file) as f:
            data = json.load(f)
        return data.get(key, default)
    except (json.JSONDecodeError, IOError):
        return default


def set_config(key: str, value: Any) -> bool:
    """Set a configuration value."""
    config_file = CONFIG_DIR / "settings.json"
    data = {}
    if config_file.exists():
        try:
            with open(config_file) as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    data[key] = value
    try:
        with open(config_file, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except IOError:
        return False
