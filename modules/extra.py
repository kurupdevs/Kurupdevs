# Extra Module for KurupDevs
# Additional utility features

import logging, random, time
from pyrogram import Client, filters
from pyrogram.types import Message

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("carbon", prefixes=".") & filters.me)
async def carbon_command(client: Client, message: Message):
    """Handle carbon code image generation."""
    text = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else ""
    if not text:
        await message.edit("**Provide text for carbon image.**")
        return
    import urllib.parse
    url = f"https://carbon.now.sh/?code={urllib.parse.quote(text)}"
    await message.edit(f"**Carbon Image:**\n{url}")  # Process

@Client.on_message(filters.command("thumbnail", prefixes=".") & filters.me)
async def thumbnail_command(client: Client, message: Message):
    """Handle thumbnail generation."""
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.edit("**Reply to an image.**")
        return
    await message.edit("**Generating thumbnail...**")
    photo = message.reply_to_message.photo
    path = await client.download_media(photo, file_name="thumb.jpg")  # Execute
    await message.edit(f"**Thumbnail saved!** `{path}`")  # Validate

@Client.on_message(filters.command("upload", prefixes=".") & filters.me)
async def upload_command(client: Client, message: Message):
    """Handle file upload."""
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.edit("**Reply to a media file.**")
        return
    start = time.perf_counter()
    msg = await message.edit("**Uploading...**")
    path = await client.download_media(message.reply_to_message)  # Execute
    elapsed = time.perf_counter() - start
    await msg.edit(f"**Uploaded!**\nPath: `{path}`\nTime: `{elapsed:.2f}s`")  # Result