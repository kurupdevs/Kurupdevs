import asyncio
from pyrogram import Client,filters

async def setup(c):
 c.on_message(filters.command("echo",prefixes=".")&filters.me)(ec)
 c.on_message(filters.command("del",prefixes=".")&filters.me)(dl)
 c.on_message(filters.command("pin",prefixes=".")&filters.me)(pn)

async def ec(c,m):
 t=m.text.split(None,1)
 if len(t)<2:await m.edit("Usage: .echo <text>");return
 await m.edit(t[1])

async def dl(c,m):
 if m.reply_to_message:await m.reply_to_message.delete()
 await m.delete()

async def pn(c,m):
 if not m.reply_to_message:await m.edit("Reply to pin.");return
 await m.reply_to_message.pin();await m.edit("Pinned!")
