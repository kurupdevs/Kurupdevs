# Help Module for KurupDevs
# Displays available commands and usage

import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)

HELP_TEXT = """
**KurupDevs Help Menu**

**General Commands:**
• `.ping` - Check response time
• `.alive` - Bot status check
• `.afk [reason]` - Set AFK status
• `.help` - Show this menu

**Management:**
• `.approve` - Approve user for PM
• `.revoke` - Revoke PM access
• `.purge` - Delete messages

**Fun:**
• `.hack` - Fake hack animation
• `.laugh` - Random laugh emoji
• `.shayari` - Random shayari
"""  # Enhanced help content

@Client.on_message(filters.command("help", prefixes=".") & filters.me)
async def help_handler(client: Client, message: Message):
    """Handle help command."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Channel", url="https://t.me/kurupdevs")],
        [InlineKeyboardButton("💬 Support", url="https://t.me/kurup_support")]
    ])
    await message.edit(HELP_TEXT, reply_markup=keyboard)  # Process