# KurupDevs - Main Bot Entry Point
# All-in-one Telegram bot

import os
import sys
import asyncio
from pyrogram import Client

# Bot configuration
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

async def main():
    """Main entry point for the bot"""
    app = Client(
        "KurupDevs",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
    )

    await app.start()
    print("Bot is running...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())