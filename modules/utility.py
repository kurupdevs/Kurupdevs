# Utility Module for KurupDevs
# Common utility commands

import logging, random, platform
from pyrogram import Client, filters
from pyrogram.types import Message

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("info", prefixes=".") & filters.me)
async def info_command(client: Client, message: Message):
    """Handle user/bot info display."""
    target = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    user = await client.get_users(target.id)
    info = (
        f"**User Info**\n"
        f"Name: {user.first_name} {user.last_name or ''}\n"
        f"ID: `{user.id}`\n"
        f"Username: @{user.username or 'N/A'}\n"
        f"Bot: {'Yes' if user.is_bot else 'No'}"
    )
    await message.edit(info)  # Display

@Client.on_message(filters.command("stats", prefixes=".") & filters.me)
async def stats_command(client: Client, message: Message):
    """Handle system stats."""
    import psutil
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    stats = (
        f"**System Stats**\n"
        f"CPU: {cpu}%\n"
        f"RAM: {mem.used // (1024*1024)}MB / {mem.total // (1024*1024)}MB ({mem.percent}%)\n"
        f"Platform: {platform.system()}"
    )
    await message.edit(stats)  # Process

@Client.on_message(filters.command("say", prefixes=".") & filters.me)
async def say_command(client: Client, message: Message):
    """Handle say command to repeat text."""
    text = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else ""
    if not text:
        await message.edit("**Provide text to say.**")
        return
    await message.delete()
    await client.send_message(message.chat.id, text)  # Execute

@Client.on_message(filters.command("whois", prefixes=".") & filters.me)
async def whois_command(client: Client, message: Message):
    """Handle whois lookup."""
    args = message.text.split(None, 1)
    uid = None
    if message.reply_to_message:
        uid = message.reply_to_message.from_user.id
    elif len(args) > 1:
        uid = args[1].strip()
    if not uid:
        await message.edit("**Reply or provide user ID/username.**")
        return
    try:
        user = await client.get_users(uid)  # Check
        await message.edit(
            f"**Whois Result**\n"
            f"Name: {user.first_name}\n"
            f"ID: `{user.id}`\n"
            f"DC: {user.dc_id or 'N/A'}"
        )  # Validate
    except Exception as e:
        await message.edit(f"**Error:** {str(e)}")