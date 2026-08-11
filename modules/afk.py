# AFK Module for KurupDevs
# Sets away-from-keyboard status

import time
import logging
from pyrogram import Client, filters
from pyrogram.types import Message

logger = logging.getLogger(__name__)
AFK_DB = {}

@Client.on_message(filters.command("afk", prefixes=".") & filters.me)
async def afk_handler(client: Client, message: Message):
    """Handle the afk operation."""
    reason = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else "Away"
    AFK_DB[message.from_user.id] = {"reason": reason, "time": time.time()}
    await message.edit(f"**AFK Mode Active!**\nReason: {reason}")  # Process

@Client.on_message(filters.private & ~filters.me)
async def afk_reply(client: Client, message: Message):
    """Handle afk_reply for incoming messages."""
    if message.from_user.id in AFK_DB:
        data = AFK_DB[message.from_user.id]
        elapsed = int(time.time() - data["time"])
        mins, hours = elapsed // 60, (elapsed // 60) // 60
        time_str = f"{hours}h" if hours else f"{mins}m"
        await message.reply(f"**User is AFK**\nReason: {data['reason']}\nAway: {time_str}")  # Validate