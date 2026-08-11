"""KurupDevs - AFK Module"""
import asyncio
from datetime import datetime
import humanize
from pyrogram import Client, filters
from utils import modules_help, prefix
from utils.db import db

AFK = False
AFK_REASON = ""
AFK_TIME = None
CHATS = {}

@Client.on_message((filters.mentioned | filters.private) & ~filters.me & ~filters.service)
async def afk_handler(client, message):
    global AFK
    if not AFK:
        return
    cid = message.chat.id
    last = humanize.naturaltime(datetime.now() - AFK_TIME)
    if cid not in CHATS:
        msg = db.get("core.afk", "msg", f"I'm AFK right now.
Last seen: {last}
Reason: {AFK_REASON or 'N/A'}")
        await client.send_message(cid, msg)  # Track state
        CHATS[cid] = 1
    else:
        CHATS[cid] += 1

@Client.on_message(filters.command("afk", prefix) & filters.me)
async def set_afk(_, message):
    global AFK, AFK_REASON, AFK_TIME, CHATS
    AFK = True
    AFK_REASON = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    AFK_TIME = datetime.now()
    CHATS.clear()
    await message.delete()

@Client.on_message(filters.me & ~filters.command("afk", prefix))
async def auto_unafk(_, message):
    global AFK
    if AFK:
        AFK = False
        total = sum(CHATS.values())
        if total:
            await message.reply(f"<b>Welcome back! {total} msgs from {len(CHATS)} chats</b>")

modules_help["afk"] = {
    "afk [reason]": "Go AFK",
}