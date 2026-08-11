"""Helper scripts for KurupDevs userbot."""
import asyncio
import logging
from typing import Optional
from pyrogram import Client
from pyrogram.types import Message

logger = logging.getLogger(__name__)


async def progress(current: int, total: int, message: Message, action: str = "Processing"):
    """Show a progress bar for uploads/downloads."""
    percent = current * 100 / total
    bar_len = 20
    filled = int(bar_len * current / total)
    bar = "█" * filled + "░" * (bar_len - filled)
    await message.edit(f"**{action}:** [{bar}] {percent:.1f}%")


async def safe_edit(message: Message, text: str):
    """Edit a message safely, catching errors."""
    try:
        await message.edit(text)
    except Exception as e:
        logger.warning(f"Failed to edit message: {e}")


async def safe_delete(message: Message):
    """Delete a message safely."""
    try:
        await message.delete()
    except Exception as e:
        logger.warning(f"Failed to delete message: {e}")


def parse_args(text: str, count: int = 2) -> list:
    """Parse command arguments from message text."""
    parts = text.split(None, count)
    if len(parts) > 1:
        return parts[1:]
    return []
