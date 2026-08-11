import random
F=["Honey never spoils.","A day on Venus > year on Venus.","Octopuses have 3 hearts."]
J=["Why atoms? They make up everything!","Fake spaghetti? Impasta!"]

async def setup(c):
 from pyrogram import filters
 c.on_message(filters.command("fact",prefixes=".")&filters.me)(fa)
 c.on_message(filters.command("joke",prefixes=".")&filters.me)(jo)

async def fa(c,m):await m.edit(f"**Fact:** {random.choice(F)}")
async def jo(c,m):await m.edit(f"**Joke:** {random.choice(J)}")
