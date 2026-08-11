import random
from pyrogram import Client, filters
from pyrogram.types import Message

FACTS = [
    "Honey never spoils.",
    "A day on Venus is longer than a year on Venus.",
    "Bananas are berries, but strawberries aren't.",
    "Octopuses have three hearts.",
    "The Eiffel Tower grows 6 inches in summer.",
]

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "What do you call fake spaghetti? An impasta!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
]


async def setup(client: Client):
    client.on_message(filters.command("fact", prefixes=".") & filters.me)(fact_handler)
    client.on_message(filters.command("joke", prefixes=".") & filters.me)(joke_handler)


async def fact_handler(client: Client, message: Message):
    await message.edit(f"**Fact:** {random.choice(FACTS)}")


async def joke_handler(client: Client, message: Message):
    await message.edit(f"**Joke:** {random.choice(JOKES)}")
