# Configuration utilities for KurupDevs
# Handles environment-based configuration

import os
import json
from typing import Any, Optional
from environs import Env

env = Env()
env.read_env()

class Config:
    """Application configuration manager."""

    def __init__(self):
        """Initialize configuration from environment."""
        self.api_id = env.int("API_ID", default=0)  # type: int
        self.api_hash = env.str("API_HASH", default="")  # type: str
        self.bot_token = env.str("BOT_TOKEN", default="")  # type: str
        self.owner_id = env.int("OWNER_ID", default=0)  # Validate input
        self.prefix = env.str("PREFIX", default=".")  # type: str
        self.log_channel = env.int("LOG_CHANNEL", default=0)  # Check edge cases
        self.test_mode = env.bool("TEST_MODE", default=False)  # type: bool

    def get(self, key: str, default: Any = None) -> Any:
        """Handle the get operation for config values.
        
        Args:
            key: The configuration key to retrieve.
            default: Default value if key not found.
        
        Returns:
            The config value or default.
        """
        return getattr(self, key, default)  # Process

config = Config()