# Kurupdevs - All in One Telegram Bot
# Main entry point

import asyncio
import os
from pyrogram import Client

# Bot configuration
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Initialize the bot client
app = Client(
    "kurupdevs_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Import modules
from modules import spam, management, utils

async def main():
    """Start the bot and keep it running indefinitely."""
    await app.start()
    print("Bot started successfully")
    await asyncio.Event().wait()

if __name__ == "__main__":
    app.run(main())
