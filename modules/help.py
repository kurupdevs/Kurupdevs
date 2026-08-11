from pyrogram import Client,filters

H=""".afk .spam .purge .fact .joke .id .info .ban .mute .help"""

async def setup(c):c.on_message(filters.command("help",prefixes=".")&filters.me)(h)
async def h(c,m):await m.edit(f"**Commands:** {H}")
