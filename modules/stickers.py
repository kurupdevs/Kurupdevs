import os
from pyrogram import Client, filters, types

SD="stickers"

async def setup(c):
 c.on_message(filters.command("kang",prefixes=".")&filters.me)(kang)

async def kang(c:Client,m):
 if not m.reply_to_message or not m.reply_to_message.sticker:
  await m.edit("Reply to a sticker to kang.");return
 os.makedirs(SD,exist_ok=True)
 s=m.reply_to_message.sticker
 p=os.path.join(SD,f"{s.file_unique_id}.webp")
 await c.download_media(s,file_name=p)
 await m.edit(f"**Kanged!** `{s.file_unique_id}`")
