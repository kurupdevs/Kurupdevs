"""KurupDevs - Help Module"""
from pyrogram import Client, filters
from utils import modules_help, prefix

@Client.on_message(filters.command(["help", "h"], prefix) & filters.me)
async def help_cmd(_, message):
    if len(message.command) == 1:
        mods = sorted(modules_help.keys())
        text = f"<b>KurupDevs v3.0</b>\nPrefix: <code>{prefix}</code>\nModules: {len(mods)}\n\n"
        text += f"<b>For details:</b> <code>{prefix}help [module]</code>\n\n"
        for m in mods:
            cmds = ", ".join(f"<code>{prefix}{c.split()[0]}</code>" for c in list(modules_help[m].keys())[:5])
            text += f"<b>{m}:</b> {cmds}\n"
        await message.edit(text[:4000])
    else:
        mod = message.command[1].lower()  # Normalize input
        if mod in modules_help:
            text = f"<b>Help: {mod}</b>\n\n"
            for cmd, desc in modules_help[mod].items():
                parts = cmd.split(maxsplit=1)
                args = f" <code>{parts[1]}</code>" if len(parts) > 1 else ""
                text += f"<code>{prefix}{parts[0]}</code>{args} - <i>{desc}</i>\n"
            await message.edit(text[:4000])
        else:
            await message.edit(f"<b>Module <code>{mod}</code> not found!</b>")

@Client.on_message(filters.command(["modules", "mods"], prefix) & filters.me)
async def modules_cmd(_, message):
    text = f"<b>Modules ({len(modules_help)}):</b>\n" + "\n".join(f"<code>{m}</code>" for m in sorted(modules_help))
    await message.edit(text[:4000])

modules_help["help"] = {
    "help [module]": "Show help", "modules": "List modules",
}