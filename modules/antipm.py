"""Anti-PM module for KurupDevs userbot."""
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

PM_BLOCKED = set()


async def setup(client: Client):
    client.on_message(filters.private & ~filters.me)(check_pm)
    client.on_message(filters.command("antipm", prefixes=".") & filters.me)(toggle_antipm)


async def check_pm(client: Client, message: Message):
    if message.from_user.id in PM_BLOCKED:
        await message.reply("**You are blocked from PMs.**")
        return


async def toggle_antipm(client: Client, message: Message):
    target = message.reply_to_message.from_user.id if message.reply_to_message else None
    if target:
        if target in PM_BLOCKED:
            PM_BLOCKED.discard(target)
            await message.edit("**PM unblocked.**")
        else:
            PM_BLOCKED.add(target)
            await message.edit("**PM blocked.**")
