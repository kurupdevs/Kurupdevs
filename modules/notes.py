"""KurupDevs - Notes & Filters"""
from pyrogram import Client, errors, filters
from utils import modules_help, prefix
from utils.db import db
from utils.scripts import format_exc

@Client.on_message(filters.command(["save"], prefix) & filters.me)
async def save_note(client, message):
    if len(message.text.split()) < 2 or not message.reply_to_message:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}save [name] (reply)</code>")
    name = message.text.split(maxsplit=1)[1].split()[0].lower()
    try:
        sid = db.get("core.notes", "storage_id", 0)
        chat = await client.get_chat(sid)
    except:
        chat = await client.create_supergroup("KurupDevs_Storage")
        db.set("core.notes", "storage_id", chat.id)
    try:
        msg_obj = await message.reply_to_message.forward(chat.id)
    except errors.ChatForwardsRestricted:
        msg_obj = await message.reply_to_message.copy(chat.id)
    db.set("core.notes", f"n_{name}", {"cid": chat.id, "mid": msg_obj.id})
    await message.edit(f"<b>Note <code>{name}</code> saved!</b>")

@Client.on_message(filters.command(["get", "note"], prefix) & filters.me)
async def get_note(client, message):
    if len(message.command) < 2:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}get [name]</code>")
    note = db.get("core.notes", f"n_{message.command[1].lower()}")
    if not note:
        return await message.edit("<b>Not found!</b>")
    try:
        await client.copy_message(message.chat.id, note["cid"], note["mid"])
        await message.delete()
    except Exception as e:
        await message.edit(format_exc(e))

@Client.on_message(filters.command(["notes"], prefix) & filters.me)
async def list_notes(_, message):
    notes = [k.replace("n_", "") for k in db.get_collection("core.notes") if k.startswith("n_")]
    if notes:
        await message.edit("<b>Notes:</b>\n" + "\n".join(f"<code>{n}</code>" for n in sorted(notes)))
    else:
        await message.edit("<b>No notes!</b>")

@Client.on_message(filters.command(["delnote"], prefix) & filters.me)
async def del_note(_, message):
    if len(message.command) < 2:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}delnote [name]</code>")
    db.remove("core.notes", f"n_{message.command[1].lower()}")
    await message.edit(f"<b>Deleted!</b>")

@Client.on_message(filters.command(["fadd"], prefix) & filters.me)
async def add_filter(client, message):
    if len(message.text.split()) < 2 or not message.reply_to_message:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}fadd [keyword] (reply)</code>")
    kw = message.text.split(maxsplit=1)[1].split()[0].lower()
    try:
        sid = db.get("core.notes", "storage_id", 0)
        chat = await client.get_chat(sid)
    except:
        chat = await client.create_supergroup("KurupDevs_Storage")
        db.set("core.notes", "storage_id", chat.id)
    try:
        msg_obj = await message.reply_to_message.forward(chat.id)
    except errors.ChatForwardsRestricted:
        msg_obj = await message.reply_to_message.copy(chat.id)
    fdata = db.get("core.filters", f"c_{message.chat.id}", {})
    fdata[kw] = {"cid": chat.id, "mid": msg_obj.id}
    db.set("core.filters", f"c_{message.chat.id}", fdata)
    await message.edit(f"<b>Filter <code>{kw}</code> added!</b>")

@Client.on_message(filters.group & ~filters.me)
async def filter_handler(client, message):
    if not message.text:
        return
    fdata = db.get("core.filters", f"c_{message.chat.id}", {})
    for kw, data in fdata.items():
        if kw in message.text.lower():
            try:
                await client.copy_message(message.chat.id, data["cid"], data["mid"])
            except:
                pass
            return

@Client.on_message(filters.command(["filters"], prefix) & filters.me)
async def list_filters(_, message):
    fdata = db.get("core.filters", f"c_{message.chat.id}", {})
    if fdata:
        await message.edit("<b>Filters:</b>\n" + "\n".join(f"<code>{k}</code>" for k in fdata))
    else:
        await message.edit("<b>No filters!</b>")

@Client.on_message(filters.command(["fdel"], prefix) & filters.me)
async def del_filter(_, message):
    if len(message.command) < 2:
        return await message.edit(f"<b>Usage:</b> <code>{prefix}fdel [keyword]</code>")
    fdata = db.get("core.filters", f"c_{message.chat.id}", {})
    if message.command[1].lower() in fdata:
        del fdata[message.command[1].lower()]
        db.set("core.filters", f"c_{message.chat.id}", fdata)
        await message.edit(f"<b>Deleted!</b>")
    else:
        await message.edit("<b>Not found!</b>")

modules_help["notes"] = {
    "save [name] [reply]*": "Save note", "get [name]*": "Get note", "notes": "List notes",
    "delnote [name]*": "Delete note", "fadd [kw] [reply]*": "Add filter",
    "filters": "List filters", "fdel [kw]*": "Delete filter",
}
