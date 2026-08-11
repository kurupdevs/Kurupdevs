#
# Kurupdevs Telegram Userbot
# Copyright (C) 2020-present Kurup
#
# Core entry point for the userbot application
#

import os
import logging
import asyncio

from pyrogram import Client, filters, idle

# Core configuration
from config import API_ID, API_HASH, BOT_TOKEN
from utils.loader import load_modules

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    """Initialize and start the userbot client."""
    app = Client(
        "kurupdevs",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
    )
    
    # Load all modules dynamically
    await load_modules(app)
    
    await app.start()
    logger.info("Kurupdevs Userbot started successfully!")
    
    await idle()
    await app.stop()


if __name__ == "__main__":
    app.run(main())
