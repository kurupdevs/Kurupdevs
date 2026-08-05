"""KurupDevs - Anti-PM Module"""
from pyrogram import Client, filters
from utils import modules_help, prefix
from utils.db import db
from utils.config import pm_limit

_warns = {}

@Client.on_message(filters.private & ~filters.me & ~filters.bot)
async def antipm_handler(client, message):
    if not db.get("core.antipm", "status", False):
        return
    uid = message.from_user.id
    if message.from_user.is_contact:
        return
    if db.get("core.antipm", f"allow_{uid}"):
        return
    me = await client.get_me()
    msg = db.get("core.antipm", "msg", f"Hi! This is {me.first_name}'s assistant. Owner is busy. Don't spam!")
    await client.send_message(uid, msg)
    _warns[uid] = _warns.get(uid, 0) + 1
    if _warns[uid] >= pm_limit:
        await client.send_message(uid, "<b>You're blocked!</b>")
        await client.block_user(uid)
        del _warns[uid]

@Client.on_message(filters.command(["antipm"], prefix) & filters.me)
async def antipm_toggle(_, message):
    cur = db.get("core.antipm", "status", False)
    new = not cur
    db.set("core.antipm", "status", new)
    await message.edit(f"<b>Anti-PM {'ON' if new else 'OFF'}!</b>")

@Client.on_message(filters.command(["a", "approve"], prefix) & filters.me)
async def approve(_, message):
    db.set("core.antipm", f"allow_{message.chat.id}", True)
    if message.chat.id in _warns:
        del _warns[message.chat.id]
    await message.edit("<b>Approved!</b>")

@Client.on_message(filters.command(["d", "disapprove"], prefix) & filters.me)
async def disapprove(_, message):
    db.remove("core.antipm", f"allow_{message.chat.id}")
    await message.edit("<b>Disapproved!</b>")

modules_help["antipm"] = {
    "antipm": "Toggle Anti-PM", "a": "Approve user", "d": "Disapprove user",
}
