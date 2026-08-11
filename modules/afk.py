import asyncio
from pyrogram import Client,filters

AFK={}

async def setup(c):
 c.on_message(filters.command("afk",prefixes=".")&filters.me)(h)
 c.on_message(filters.private&~filters.me)(chk)

async def h(c,m):
 r=m.text.split(None,1)[1]if len(m.text.split())>1 else"AFK"
 AFK[m.from_user.id]=r;await m.edit(f"**AFK:** {r}")

async def chk(c,m):
 if m.from_user and m.from_user.id in AFK:
  await m.reply(f"User is AFK: {AFK[m.from_user.id]}")
