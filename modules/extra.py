"""KurupDevs - Extra Module"""
import aiohttp
from io import BytesIO
from pyrogram import Client, filters
from utils import modules_help, prefix
from utils.scripts import format_exc, with_reply, resize_image

@Client.on_message(filters.command(["reply", "r"], prefix) & filters.me)
async def reply_cmd(_, message):
    if not message.reply_to_message or len(message.command) < 2:
        return await message.edit("<b>Reply + provide text!</b>")
    await message.delete()
    await message.reply_to_message.reply(" ".join(message.command[1:]))

@Client.on_message(filters.command(["copy"], prefix) & filters.me)
@with_reply
async def copy_cmd(client, message):
    await message.delete()
    await message.reply_to_message.copy(message.chat.id)

@Client.on_message(filters.command(["fwd", "forward"], prefix) & filters.me)
@with_reply
async def fwd_cmd(client, message):
    target = message.command[1] if len(message.command) > 1 else None
    if not target:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}fwd [chat] (reply)</code>")
    try:
        await message.reply_to_message.forward(int(target) if target.lstrip("-").isdigit() else target)
        await message.edit("<b>Forwarded!</b>")
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["whisper", "wspr"], prefix) & filters.me)
async def whisper_cmd(client, message):
    if len(message.command) < 3:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}whisper [user] [text]</code>")
    try:
        target = int(message.command[1]) if message.command[1].lstrip("-").isdigit() else message.command[1]
        await client.send_message(target, f"<b>Whisper:</b>\n<i>{' '.join(message.command[2:])}</i>")
        await message.edit("<b>Whisper sent!</b>")
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["groupdata", "gpdata"], prefix) & filters.me)
async def gpdata_cmd(client, message):
    if message.chat.type == "private":
        return await message.edit("<b>Private chat!</b>")
    c = message.chat
    try:
        cnt = await client.get_chat_members_count(c.id)
    except:
        cnt = "?"
    await message.edit(f"<b>{c.title}</b>\n<b>ID:</b> <code>{c.id}</code>\n<b>Members:</b> {cnt}")

@Client.on_message(filters.command(["members"], prefix) & filters.me)
async def members_cmd(client, message):
    if message.chat.type == "private":
        return await message.edit("<b>Private chat!</b>")
    try:
        cnt = await client.get_chat_members_count(message.chat.id)
        await message.edit(f"<b>Members:</b> {cnt}")
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["q", "quote"], prefix) & filters.me)
@with_reply
async def quote_cmd(client, message):
    await message.edit("<b>Generating quote...</b>")
    try:
        q = message.reply_to_message
        user = q.from_user or q.sender_chat
        name = user.first_name if hasattr(user, 'first_name') else user.title
        txt = q.text or q.caption or "Media"
        from utils.config import quotes_api
        async with aiohttp.ClientSession() as s:
            async with s.post(quotes_api, json={"messages": [{"text": txt, "author": {"id": user.id, "name": name, "rank": "", "avatar": "", "via_bot": ""}, "reply": {}, "media": "", "entities": []}], "quote_color": "#162330", "text_color": "#fff"}) as r:
                content = await r.read()
        img = resize_image(BytesIO(content), img_type="WEBP")
        await client.send_sticker(message.chat.id, img)
        await message.delete()
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["webss", "ss"], prefix) & filters.me)
async def webss_cmd(client, message):
    if len(message.command) < 2:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}webss [url]</code>")
    url = message.command[1]
    if not url.startswith("http"):
        url = "https://" + url
    await message.edit("<b>Taking screenshot...</b>")
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"https://image.thum.io/get/{url}") as r:
                img = BytesIO(await r.read())
                img.name = "ss.jpg"
        await client.send_photo(message.chat.id, img, caption=f"<b>{url}</b>")
        await message.delete()
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["carbon"], prefix) & filters.me)
async def carbon_cmd(client, message):
    code = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
    if not code:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}carbon [code/reply]</code>")
    await message.edit("<b>Generating...</b>")
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post("https://carbonara.solopov.dev/api/cook", json={"code": code, "backgroundColor": "#1F1F1F"}) as r:
                img = BytesIO(await r.read())
                img.name = "carbon.png"
        await client.send_photo(message.chat.id, img, caption="<b>KurupDevs</b>")
        await message.delete()
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["shorten", "short"], prefix) & filters.me)
async def shorten_cmd(_, message):
    url = message.command[1] if len(message.command) > 1 else (message.reply_to_message.text if message.reply_to_message else None)
    if not url:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}shorten [url]</code>")
    await message.edit("<b>Shortening...</b>")
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"https://tinyurl.com/api-create.php?url={url}") as r:
                short = await r.text()
        await message.edit(f"<b>{short}</b>")
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["edit", "e"], prefix) & filters.me)
async def edit_cmd(_, message):
    if not message.reply_to_message or not message.reply_to_message.outgoing:
        return await message.edit("<b>Reply to YOUR message!</b>")
    if len(message.command) < 2:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}edit [text]</code>")
    try:
        await message.reply_to_message.edit(" ".join(message.command[1:]))
        await message.delete()
    except Exception as e:
        await message.edit(format_exc(e))

modules_help["extra"] = {
    "reply [text] [reply]*": "Quick reply", "copy [reply]*": "Copy message",
    "fwd [chat] [reply]*": "Forward", "whisper [user] [text]*": "Whisper",
    "groupdata": "Group info", "members": "Member count", "q [reply]*": "Quote",
    "webss [url]*": "Screenshot", "carbon [code]*": "Carbon",
    "shorten [url]*": "Shorten URL", "edit [text] [reply]*": "Edit msg",
}
