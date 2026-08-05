"""KurupDevs - Spam Module"""
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import modules_help, prefix

COOLDOWNS = {"spam": 0.15, "fastspam": 0.01, "slowspam": 0.9, "statspam": 0.1, "delayspam": 1.5, "bigspam": 0.05}
RAID_MSGS = ["☠️ RAID BY KURUPDEVS ☠️", "👿 TARGET ACQUIRED 👿", "💀 NUKED 💀", "🔥 BURN BABY BURN 🔥", "⚡ THUNDER ⚡", "💥 BOOM 💥", "🎯 HEADSHOT 🎯"]

@Client.on_message(filters.command(list(COOLDOWNS.keys()), prefix) & filters.me)
async def spam_handler(client, message):
    cmd = message.command[0]
    if len(message.command) < 3:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}{cmd} [amount] [text]</code>")
    try:
        amount = min(int(message.command[1]), 1000)
    except ValueError:
        return await message.edit("<b>Amount must be a number!</b>")
    text = " ".join(message.command[2:])
    cooldown = COOLDOWNS[cmd]
    await message.delete()
    for _ in range(amount):
        try:
            if message.reply_to_message:
                sent = await message.reply_to_message.reply(text)
            else:
                sent = await client.send_message(message.chat.id, text)
            if cmd == "statspam":
                await asyncio.sleep(0.1)
                await sent.delete()
        except Exception:
            pass
        await asyncio.sleep(cooldown)

@Client.on_message(filters.command(["raid"], prefix) & filters.me)
async def raid_handler(client, message):
    if not message.reply_to_message:
        return await message.edit("<b>Reply to a user!</b>")
    try:
        amount = min(int(message.command[1]), 500) if len(message.command) > 1 else 10
    except ValueError:
        return await message.edit("<b>Amount must be a number!</b>")
    await message.delete()
    user = message.reply_to_message.from_user
    mention = user.mention if user else "User"
    for _ in range(amount):
        try:
            await message.reply_to_message.reply(f"{mention} {random.choice(RAID_MSGS)}")
            await asyncio.sleep(0.1)
        except Exception:
            pass

modules_help["spam"] = {
    "spam [amount] [text]": "Spam (0.15s)",
    "fastspam [amount] [text]": "Fast spam (0.01s)",
    "slowspam [amount] [text]": "Slow spam (0.9s)",
    "statspam [amount] [text]": "Spam + delete",
    "delayspam [amount] [text]": "Delayed (1.5s)",
    "bigspam [amount] [text]": "Big spam (0.05s)",
    "raid [amount] [reply]*": "Raid a user",
}
