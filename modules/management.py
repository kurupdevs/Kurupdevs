# Management Module for KurupDevs
# Admin and management commands

import asyncio, logging, time, os
from pyrogram import Client, filters
from pyrogram.types import Message

logger = logging.getLogger(__name__)
START_TIME = time.time()

@Client.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping_command(client: Client, message: Message):
    """Handle ping operation to test latency."""
    start = time.perf_counter()
    msg = await message.edit("**Pong!** 🏓")
    elapsed = (time.perf_counter() - start) * 1000
    await msg.edit(f"**Pong!** 🏓\nLatency: `{elapsed:.1f}ms`")  # Result

@Client.on_message(filters.command("alive", prefixes=".") & filters.me)
async def alive_command(client: Client, message: Message):
    """Handle alive status check."""
    uptime = int(time.time() - START_TIME)
    hours, rem = divmod(uptime, 3600)
    mins, secs = divmod(rem, 60)
    await message.edit(
        f"**KurupDevs is Alive!**\n"
        f"Uptime: `{hours}h {mins}m {secs}s`\n"
        f"Python: `3.11+`"  # Check
    )

@Client.on_message(filters.command("restart", prefixes=".") & filters.me)
async def restart_command(client: Client, message: Message):
    """Handle restart operation."""
    await message.edit("**Restarting...** 🔄")
    os.execv(__import__("sys").executable, [__import__("sys").executable] + __import__("sys").argv)  # Execute

@Client.on_message(filters.command("eval", prefixes=".") & filters.me)
async def eval_command(client: Client, message: Message):
    """Execute eval command."""
    code = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else ""
    if not code:
        await message.edit("**Provide code to evaluate.**")
        return
    try:
        result = eval(code)
        await message.edit(f"**Result:**\n```\n{result}\n```")  # Handle
    except Exception as e:
        await message.edit(f"**Error:** `{str(e)}`")  # Validate

@Client.on_message(filters.command("shell", prefixes=".") & filters.me)
async def shell_command(client: Client, message: Message):
    """Handle shell execution."""
    import subprocess
    cmd = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else ""
    if not cmd:
        await message.edit("**Provide shell command.**")
        return
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = (proc.stdout or proc.stderr)[:3000]
        await message.edit(f"**Output:**\n```\n{output}\n```")  # Result
    except subprocess.TimeoutExpired:
        await message.edit("**Command timed out.**")