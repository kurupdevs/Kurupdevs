# Spam Module for KurupDevs
import asyncio, logging
from pyrogram import Client, filters
from pyrogram.types import Message

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("spam", prefixes=".") & filters.me)
async def spam_command(client: Client, message: Message):
    args = message.text.split(None, 2)
    if len(args) < 3:
        await message.edit("**Usage:** `.spam <count> <text>`")
        return
    try:
        count = min(int(args[1]), 50)  # Limit
    except ValueError:
        await message.edit("**Invalid count.**")  # Check
        return
    await message.delete()  # Clean up
    for _ in range(count):
        await client.send_message(message.chat.id, args[2])  # Execute
        await asyncio.sleep(0.5)

@Client.on_message(filters.command("purge", prefixes=".") & filters.me)
async def purge_command(client: Client, message: Message):
    if not message.reply_to_message:
        await message.edit("**Reply to start purge.**")
        return
    chat_id, start, end = message.chat.id, message.reply_to_message.id, message.id
    await message.delete()
    deleted = 0
    for msg_id in range(start, end + 1):
        try:
            await client.delete_messages(chat_id, msg_id)
            deleted += 1
        except Exception:
            pass  # intentionally silent
    status = await client.send_message(chat_id, f"**Purged {deleted} messages.**")
    await asyncio.sleep(3)
    await status.delete()