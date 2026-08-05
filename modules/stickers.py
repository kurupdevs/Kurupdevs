"""KurupDevs - Stickers Module"""
import os
from io import BytesIO
from pyrogram import Client, filters
from utils import modules_help, prefix
from utils.scripts import format_exc, with_reply, resize_image

@Client.on_message(filters.command(["kang"], prefix) & filters.me)
@with_reply
async def kang(client, message):
    if len(message.command) < 2:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}kang [pack] [emoji]</code>")
    await message.edit("<b>Kanging...</b>")
    pack = message.command[1]
    emoji = message.command[2] if len(message.command) > 2 else "✨"
    try:
        path = await message.reply_to_message.download()
        img = resize_image(path)
        if os.path.exists(path):
            os.remove(path)
        await client.send_document("me", img, caption=f"<b>Pack: <code>{pack}</code></b>")
        await message.edit(f"<b>Sticker saved! Add to @Stickers with /addsticker</b>")
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["stp", "sticker2png"], prefix) & filters.me)
@with_reply
async def stp(client, message):
    try:
        await message.edit("<b>Converting...</b>")
        path = await message.reply_to_message.download()
        with open(path, "rb") as f:
            content = f.read()
        if os.path.exists(path):
            os.remove(path)
        img = BytesIO(content)
        img.name = "sticker.png"
        await client.send_document(message.chat.id, img, caption="<b>KurupDevs</b>")
        await message.delete()
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["resize"], prefix) & filters.me)
@with_reply
async def resize_cmd(client, message):
    try:
        await message.edit("<b>Resizing...</b>")
        path = await message.reply_to_message.download()
        img = resize_image(path)
        img.name = "resized.png"
        if os.path.exists(path):
            os.remove(path)
        await client.send_document(message.chat.id, img, caption="<b>KurupDevs</b>")
        await message.delete()
    except Exception as e:
        await message.edit(format_exc(e))

modules_help["stickers"] = {
    "kang [reply]* [pack]* [emoji]": "Steal sticker",
    "stp [reply]*": "Sticker to PNG",
    "resize [reply]*": "Resize image",
}
