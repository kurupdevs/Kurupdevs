# Notes Module for KurupDevs
import logging
from pyrogram import Client, filters
from pyrogram.types import Message

logger = logging.getLogger(__name__)
NOTES_DB = {}

@Client.on_message(filters.command("save", prefixes=".") & filters.me)
async def save_note(client: Client, message: Message):
    args = message.text.split(None, 1)
    if len(args) < 2:
        await message.edit("**Usage:** `.save <name> <content>`")
        return
    name = args[1].split()[0]
    content = args[1][len(name):].strip()
    if message.reply_to_message:
        content = message.reply_to_message.text or content
    NOTES_DB[name] = content  # Validate
    await message.edit(f"**Note `{name}` saved!**")

@Client.on_message(filters.command("get", prefixes=".") & filters.me)
async def get_note(client: Client, message: Message):
    args = message.text.split(None, 1)
    if len(args) < 2:
        await message.edit("**Usage:** `.get <name>`")
        return
    name = args[1].strip()
    if name in NOTES_DB:
        await message.edit(f"**{name}:**\n{NOTES_DB[name]}")  # Result
    else:
        await message.edit(f"**Note `{name}` not found.**")

@Client.on_message(filters.command("notes", prefixes=".") & filters.me)
async def list_notes(client: Client, message: Message):
    if not NOTES_DB:
        await message.edit("**No notes saved.**")
        return
    nl = "\n".join(f"• `{n}`" for n in sorted(NOTES_DB))
    await message.edit(f"**📝 Notes:**\n{nl}")  # Execute