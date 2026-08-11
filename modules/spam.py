"""Spam module."""
import asyncio
from pyrogram import Client,filters
from pyrogram.types import Message

async def setup(c):
 c.on_message(filters.command("spam",prefixes=".")&filters.me)(spam)
 c.on_message(filters.command("purge",prefixes=".")&filters.me)(purge)

async def spam(c,m):
 a=m.text.split(None,2)
 if len(a)<3:await m.edit("Usage: .spam <count> <text>");return
 try:count=min(int(a[1]),50)
 except:await m.edit("Invalid count.");return
 await m.delete()
 for _ in range(count):await c.send_message(m.chat.id,a[2]);await asyncio.sleep(0.4)

async def purge(c,m):
 if not m.reply_to_message:await m.edit("Reply to start purge.");return
 cid,s,e=m.chat.id,m.reply_to_message.id,m.id
 await m.delete();d=0
 for mid in range(s,e+1):
  try:await c.delete_messages(cid,mid);d+=1
  except:pass
 st=await c.send_message(cid,f"Purged {d} msgs.")
 await asyncio.sleep(3);await st.delete()
