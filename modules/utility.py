import asyncio
from pyrogram import Client,filters

async def setup(c):
 c.on_message(filters.command("id",prefixes=".")&filters.me)(id_)
 c.on_message(filters.command("info",prefixes=".")&filters.me)(inf)

async def id_(c,m):
 cid=m.chat.id;uid=m.reply_to_message.from_user.id if m.reply_to_message else m.from_user.id
 await m.edit(f"**Chat ID:** `{cid}`\n**User ID:** `{uid}`")

async def inf(c,m):
 u=m.reply_to_message.from_user if m.reply_to_message else m.from_user
 t=f"**Info:**\nName: {u.first_name}\nID: `{u.id}`\n@{u.username or 'None'}"
 await m.edit(t)
