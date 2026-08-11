"""Notes module for KurupDevs userbot."""
import json
from pyrogram import Client, filters
from pyrogram.types import Message

NOTES_FILE = "notes.json"


def _load():
    try:
        with open(NOTES_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)


async def setup(client: Client):
    client.on_message(filters.command("save", prefixes=".") & filters.me)(save_cmd)
    client.on_message(filters.command("get", prefixes=".") & filters.me)(get_cmd)


async def save_cmd(client: Client, message: Message):
    args = message.text.split(None, 2)
    if len(args) < 3:
        await message.edit("**Usage:** `.save <name> <content>`")
        return
    notes = _load()
    notes[args[1]] = args[2]
    _save(notes)
    await message.edit(f"**Saved:** `{args[1]}`")


async def get_cmd(client: Client, message: Message):
    args = message.text.split(None, 1)
    if len(args) < 2:
        await message.edit("**Usage:** `.get <name>`")
        return
    notes = _load()
    await message.edit(notes.get(args[1], "Not found."))
