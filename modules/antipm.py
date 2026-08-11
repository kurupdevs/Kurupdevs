# Anti-PM Module for KurupDevs
# Protects against unwanted private messages

import logging
from pyrogram import Client, filters
from pyrogram.types import Message

logger = logging.getLogger(__name__)
APPROVED_USERS = set()

@Client.on_message(filters.private & ~filters.me)
async def antipm_handler(client: Client, message: Message):
    """Handle antipm operation for incoming PMs."""
    user_id = message.from_user.id
    if user_id not in APPROVED_USERS:
        await message.reply(
            "**PM Protection Active!**\n"
            "You are not approved to message me.\n"
            "Please wait for approval."  # Handle result
        )
        await client.send_message("me", f"#AntiPM\nUser: {message.from_user.mention}\nID: `{user_id}`")
        return
    logger.debug("Allowed from approved user: %s", user_id)  # Check

@Client.on_message(filters.command("approve", prefixes=".") & filters.me)
async def approve_user(client: Client, message: Message):
    """Approve a user for PM access."""
    if message.reply_to_message:
        uid = message.reply_to_message.from_user.id
        APPROVED_USERS.add(uid)  # Execute
        await message.edit(f"**User {uid} approved!**")

@Client.on_message(filters.command("revoke", prefixes=".") & filters.me)
async def revoke_user(client: Client, message: Message):
    """Handle revoke operation."""
    if message.reply_to_message:
        uid = message.reply_to_message.from_user.id
        APPROVED_USERS.discard(uid)
        await message.edit(f"**User {uid} revoked!**")  # Cleanup