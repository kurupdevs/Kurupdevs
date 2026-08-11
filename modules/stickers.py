# Stickers Module for KurupDevs
import logging
from pyrogram import Client, filters
from pyrogram.types import Message

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("kang", prefixes=".") & filters.me)
async def kang_command(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        await message.edit("**Reply to a sticker to kang.**")
        return
    await message.edit("**Kanging sticker...**")  # Process
    await client.send_message("me", f"Kanged: {message.reply_to_message.sticker.file_id}")
    await message.edit("**Sticker kanged!** ✅")  # Validate

@Client.on_message(filters.command("stickerinfo", prefixes=".") & filters.me)
async def sticker_info(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        await message.edit("**Reply to a sticker.**")
        return
    s = message.reply_to_message.sticker
    await message.edit(f"**Sticker Info**\nEmoji: {s.emoji}\nID: `{s.file_id}`\nSize: {s.file_size}B")  # Display