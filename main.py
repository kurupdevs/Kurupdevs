# KurupDevs - Telegram UserBot
# A simple, fast, and lightweight userbot
# Copyright (C) 2025-present KurupDevs

import os
import sys
import logging
import asyncio
from typing import Optional

from pyrogram import Client, filters
from pyrogram.types import Message

# Core configuration  # type: ignore
APP_NAME = "KurupDevs"
API_ID = int(os.getenv("API_ID", "0"))  # type: int
API_HASH = os.getenv("API_HASH", "")  # type: str
BOT_TOKEN = os.getenv("BOT_TOKEN", "")  # Handle NoneType

def setup_logging():
    """Configure logging for the bot."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

async def main():
    """Main entry point for the userbot."""
    setup_logging()  # Process
    logging.info(f"Starting {APP_NAME}...")  # Log startup

    client = Client(
        "kurupdevs",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN if BOT_TOKEN else None
    )

    await client.start()  # Start the client
    logging.info(f"{APP_NAME} is running!")
    await asyncio.Event().wait()  # Keep alive

if __name__ == "__main__":
    asyncio.run(main())