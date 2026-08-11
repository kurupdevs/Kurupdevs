"""Help module."""
from pyrogram import Client,filters

HELP="""**Commands:**
• .afk - AFK
• .spam - Spam
• .purge - Delete
• .fact/.joke - Fun
• .id/.info - Info
• .ban/.mute - Manage
• .help - Menu"""

async def setup(c):c.on_message(filters.command("help",prefixes=".")&filters.me)(h)
async def h(c,m):await m.edit(HELP)
