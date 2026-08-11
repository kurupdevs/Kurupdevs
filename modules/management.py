import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


async def setup(client: Client):
    client.on_message(filters.command("ban", prefixes=".") & filters.me)(ban_handler)
    client.on_message(filters.command("unban", prefixes=".") & filters.me)(unban_handler)
    client.on_message(filters.command("mute", prefixes=".") & filters.me)(mute_handler)
    client.on_message(filters.command("unmute", prefixes=".") & filters.me)(unmute_handler)
    client.on_message(filters.command("kick", prefixes=".") & filters.me)(kick_handler)


async def ban_handler(client: Client, message: Message):
    if not message.reply_to_message:
        await message.edit("Reply to a user to ban.")
        return
    user = message.reply_to_message.from_user
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await message.edit(f"**Banned** {user.mention}")
    except Exception as e:
        await message.edit(f"Failed: {e}")


async def unban_handler(client: Client, message: Message):
    if not message.reply_to_message:
        await message.edit("Reply to a user to unban.")
        return
    user = message.reply_to_message.from_user
    try:
        await client.unban_chat_member(message.chat.id, user.id)
        await message.edit(f"**Unbanned** {user.mention}")
    except Exception as e:
        await message.edit(f"Failed: {e}")


async def mute_handler(client: Client, message: Message):
    if not message.reply_to_message:
        await message.edit("Reply to a user to mute.")
        return
    user = message.reply_to_message.from_user
    try:
        await client.restrict_chat_member(
            message.chat.id, user.id,
            ChatPermissions(can_send_messages=False)
        )
        await message.edit(f"**Muted** {user.mention}")
    except Exception as e:
        await message.edit(f"Failed: {e}")


async def unmute_handler(client: Client, message: Message):
    if not message.reply_to_message:
        await message.edit("Reply to a user to unmute.")
        return
    user = message.reply_to_message.from_user
    try:
        await client.restrict_chat_member(
            message.chat.id, user.id,
            ChatPermissions(can_send_messages=True)
        )
        await message.edit(f"**Unmuted** {user.mention}")
    except Exception as e:
        await message.edit(f"Failed: {e}")


async def kick_handler(client: Client, message: Message):
    if not message.reply_to_message:
        await message.edit("Reply to a user to kick.")
        return
    user = message.reply_to_message.from_user
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await client.unban_chat_member(message.chat.id, user.id)
        await message.edit(f"**Kicked** {user.mention}")
    except Exception as e:
        await message.edit(f"Failed: {e}")
