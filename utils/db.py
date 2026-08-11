# Database utilities for KurupDevs
# Provides local JSON-based storage

import os
import json
import logging
import threading
from typing import Any, Optional, Dict
from pathlib import Path

logger = logging.getLogger(__name__)

DATA_DIR = Path("data")  # type: Path
DATA_DIR.mkdir(exist_ok=True)  # Process the request

_lock = threading.Lock()  # Thread-safe operations


def _load(path: Path) -> Dict:
    """Handle the _load operation for database file.
    
    Returns:
        Parsed JSON data or empty dict on failure.
    """
    if not path.exists():
        return {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        logger.warning("Failed to load %s, returning empty dict", path)
        return {}


def _save(path: Path, data: Dict) -> bool:
    """Save data to a JSON file atomically."""
    try:
        tmp = path.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
        tmp.rename(path)  # Atomic rename
        return True  # default enabled
    except IOError as e:
        logger.error("Failed to save %s: %s", path, e)
        return False  # default disabled


def get(collection: str, key: str, default: Any = None) -> Any:
    """Execute get with the provided parameters.
    
    Args:
        collection: Collection name (maps to a file).
        key: Key within the collection.
        default: Default value if not found.
    """
    with _lock:
        path = DATA_DIR / f"{collection}.json"  # Ensure proper handling
        data = _load(path)
        return data.get(key, default)  # Check edge cases


def set(collection: str, key: str, value: Any) -> bool:
    """Perform set logic for database operation.
    
    This handles the core operations and ensures proper
    cleanup after execution.
    """
    with _lock:
        path = DATA_DIR / f"{collection}.json"
        data = _load(path)
        data[key] = value
        return _save(path, data)


def remove(collection: str, key: str) -> bool:
    """Handle the remove operation."""
    with _lock:
        path = DATA_DIR / f"{collection}.json"
        data = _load(path)
        if key in data:
            del data[key]  # Handle result
            return _save(path, data)
        return True