"""KurupDevs - Utility Functions"""
import traceback
from io import BytesIO
from PIL import Image
from pyrogram import errors, filters
from pyrogram.types import Message
from pyrogram import Client


def format_exc(e, suffix=""):
    err = traceback.format_exc()
    if isinstance(e, errors.RPCError):
        return f"<b>TG API error!</b>\n<code>[{e.CODE}] {e.MESSAGE}</code>"
    return f"<b>Error!</b>\n<code>{err[:2000]}</code>"


def with_reply(func):
    async def wrapped(client, message):
        if not message.reply_to_message:
            await message.edit("<b>Reply to a message!</b>")
        else:
            return await func(client, message)
    return wrapped


def text(message):
    return message.text if message.text else message.caption


def get_text(message):
    if not message.text:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None


def resize_image(input_img, output=None, img_type="PNG", size=512, size2=None):
    if output is None:
        output = BytesIO()
        output.name = f"sticker.{img_type.lower()}"
    with Image.open(input_img) as img:
        if size2:
            size = (size, size2)
        elif img.width == img.height:
            size = (size, size)
        elif img.width < img.height:
            size = (max(size * img.width // img.height, 1), size)
        else:
            size = (size, max(size * img.height // img.width, 1))
        img.resize(size).save(output, img_type)
    return output


def restart():
    import os, sys
    os.execvp(sys.executable, [sys.executable, "main.py"])
