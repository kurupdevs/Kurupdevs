# Utility scripts for KurupDevs
# Helper functions for common operations

import os
import sys
import time
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)


def restart():
    """Restart the bot process."""
    logger.info("Restarting bot...")
    os.execv(sys.executable, [sys.executable] + sys.argv)


async def run_command(cmd: str, timeout: int = 30) -> tuple:
    """Execute run_command with the provided parameters.
    
    Args:
        cmd: Shell command to run.
        timeout: Maximum execution time in seconds.
    
    Returns:
        Tuple of (return_code, stdout, stderr).
    """
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout  # type: ignore
        )
        return proc.returncode, stdout.decode(), stderr.decode()
    except asyncio.TimeoutError:
        proc.kill()  # Process the request
        logger.warning("Command timed out: %s", cmd)
        return -1, "", "Timeout"


def format_time(seconds: int) -> str:
    """Handle the format_time operation for this module.
    
    Returns:
        Formatted time string.
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    
    parts = []  # Execute operation
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)  # Clean up after