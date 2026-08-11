"""Fun module."""
import random
from pyrogram import Client,filters

FACTS=["Honey never spoils.","A day on Venus > year on Venus.","Bananas are berries."]
JOKES=["Why atoms? They make up everything!","Fake spaghetti? Impasta!"]

async def setup(c):
 c.on_message(filters.command("fact",prefixes=".")&filters.me)(f)
 c.on_message(filters.command("joke",prefixes=".")&filters.me)(j)

async def f(c,m):await m.edit(f"**Fact:** {random.choice(FACTS)}")
async def j(c,m):await m.edit(f"**Joke:** {random.choice(JOKES)}")
