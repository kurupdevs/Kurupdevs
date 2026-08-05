"""KurupDevs - Fun Module"""
import random
from datetime import datetime
import aiohttp
from pyrogram import Client, filters
from utils import modules_help, prefix
from utils.scripts import get_text, with_reply

@Client.on_message(filters.command(["ping", "p"], prefix) & filters.me)
async def ping_cmd(client, message):
    start = datetime.now()
    msg = await message.edit("<b>Pong!</b>")
    end = datetime.now()
    await msg.edit(f"<b>Pong!</b> <code>{(end-start).total_seconds()*1000:.0f}ms</code>")

@Client.on_message(filters.command(["alive"], prefix) & filters.me)
async def alive_cmd(client, message):
    me = await client.get_me()
    await message.edit(f"<b>KurupDevs v3.0</b>\nOwner: {me.mention}\nPrefix: <code>{prefix}</code>")

@Client.on_message(filters.command(["couples", "couple"], prefix) & filters.me)
async def couples_cmd(client, message):
    if message.chat.type == "private":
        return await message.edit("<b>Group only!</b>")
    await message.edit("<b>Finding couples...</b>")
    members = [m.user async for m in client.get_chat_members(message.chat.id, limit=50) if not m.user.is_bot]
    if len(members) < 2:
        return await message.edit("<b>Not enough members!</b>")
    u1, u2 = random.sample(members, 2)
    love = random.randint(40, 100)
    await message.edit(f"<b>Couple:</b> {u1.mention} + {u2.mention}\n<b>Love:</b> {love}%")

@Client.on_message(filters.command(["dice"], prefix) & filters.me)
async def dice_cmd(client, message):
    await client.send_dice(message.chat.id, "🎲")
    await message.delete()

@Client.on_message(filters.command(["truth"], prefix) & filters.me)
async def truth_cmd(_, message):
    qs = ["What's your biggest fear?", "Who was your first crush?", "Last lie you told?",
          "Most embarrassing moment?", "Secret talent?"]
    await message.edit(f"<b>TRUTH:</b>\n<i>{random.choice(qs)}</i>")

@Client.on_message(filters.command(["dare"], prefix) & filters.me)
async def dare_cmd(_, message):
    ds = ["Send a voice note singing!", "Change your name for 1hr!", "Post a selfie!",
          "Send your last 5 emojis!", "Don't use emojis for 1hr!"]
    await message.edit(f"<b>DARE:</b>\n<i>{random.choice(ds)}</i>")

@Client.on_message(filters.command(["joke"], prefix) & filters.me)
async def joke_cmd(_, message):
    js = ["Why don't scientists trust atoms? They make up everything!",
          "Parallel lines have so much in common. Shame they'll never meet.",
          "I told my wife she drew eyebrows too high. She looked surprised."]
    await message.edit(f"<b>Joke:</b>\n<i>{random.choice(js)}</i>")

@Client.on_message(filters.command(["shayari"], prefix) & filters.me)
async def shayari_cmd(_, message):
    ss = ["Zindagi ek kitaab hai, har din naya panna ❤️",
          "Mohabbat mein haar kar bhi jeetne ka maza kuch aur hai 🌹"]
    await message.edit(f"<b>Shayari:</b>\n<i>{random.choice(ss)}</i>")

@Client.on_message(filters.command(["figlet"], prefix) & filters.me)
async def figlet_cmd(_, message):
    if len(message.command) < 2:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}figlet [text]</code>")
    try:
        import pyfiglet
        result = pyfiglet.figlet_format(" ".join(message.command[1:]))
        await message.edit(f"<pre>{result}</pre>")
    except ImportError:
        await message.edit("<b>Install pyfiglet!</b>")
    except Exception as e:
        await message.edit(f"<b>Error:</b> {e}")

@Client.on_message(filters.command(["hug"], prefix) & filters.me)
@with_reply
async def hug_cmd(_, message):
    user = message.reply_to_message.from_user
    await message.edit(f"{message.from_user.mention} hugs {user.mention} 🤗")

@Client.on_message(filters.command(["slap"], prefix) & filters.me)
@with_reply
async def slap_cmd(_, message):
    user = message.reply_to_message.from_user
    await message.edit(f"{message.from_user.mention} slaps {user.mention} 👋")

@Client.on_message(filters.command(["kiss"], prefix) & filters.me)
@with_reply
async def kiss_cmd(_, message):
    user = message.reply_to_message.from_user
    await message.edit(f"{message.from_user.mention} kisses {user.mention} 😘")

@Client.on_message(filters.command(["fakeinfo"], prefix) & filters.me)
async def fakeinfo_cmd(_, message):
    if len(message.command) < 2:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}fakeinfo [country]</code>")
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"https://randomuser.me/api/?nat={message.command[1].upper()}") as r:
                d = (await r.json())["results"][0]
        await message.edit(f"<b>Fake ID:</b> {d['name']['first']} {d['name']['last']}\n<b>Email:</b> {d['email']}\n<b>Phone:</b> {d['phone']}\n<b>City:</b> {d['location']['city']}")
    except Exception as e:
        await message.edit(f"<b>Error:</b> {e}")

modules_help["fun"] = {
    "ping": "Check latency", "alive": "Bot status",
    "couples": "Find couples", "dice": "Roll dice",
    "truth": "Truth question", "dare": "Dare challenge",
    "joke": "Random joke", "shayari": "Hindi shayari",
    "figlet [text]*": "ASCII art", "hug [reply]*": "Hug someone",
    "slap [reply]*": "Slap someone", "kiss [reply]*": "Kiss someone",
    "fakeinfo [country]*": "Fake identity",
}
