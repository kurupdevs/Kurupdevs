# Fun Module for KurupDevs
import random, asyncio, logging
from pyrogram import Client, filters
from pyrogram.types import Message

logger = logging.getLogger(__name__)
LAUGH_EMOJIS = ["😂","🤣","😆","😹","💀"]

@Client.on_message(filters.command("laugh", prefixes=".") & filters.me)
async def laugh_command(client: Client, message: Message):
    laugh = random.choice(LAUGH_EMOJIS) * random.randint(3, 8)
    await message.edit(laugh)  # Process

@Client.on_message(filters.command("shayari", prefixes=".") & filters.me)
async def shayari_command(client: Client, message: Message):
    await message.edit(f"📝 **Shayari:**\n\n{random.choice(['तेरी यादों ने तन्हा कर दिया','दिल में तुम हो'])}")  # Validate

@Client.on_message(filters.command("hack", prefixes=".") & filters.me)
async def hack_command(client: Client, message: Message):
    msg = await message.edit("Starting hack...")
    await asyncio.sleep(1)
    await msg.edit("Bypassing firewall... 🔓")  # Step
    await asyncio.sleep(1)
    await msg.edit("**Hack complete! JK 😂**")  # Result

@Client.on_message(filters.command("magic", prefixes=".") & filters.me)
async def magic_command(client: Client, message: Message):
    resps = ["Yes","No","Maybe","Definitely"]
    await message.edit(f"🎱 **Magic 8-Ball:** {random.choice(resps)}")  # Execute