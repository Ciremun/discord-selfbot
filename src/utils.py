import json
from typing import Optional, Iterable

import discord

unicode_emojis = json.load(open('emojis.json', encoding='utf-8'))

async def send_error(error_message: str, message: discord.Message, *, delay: Optional[float] = None):
    message = await message.channel.send(error_message)
    await message.delete(delay=delay)

def lookahead(iterable: Iterable):
    it = iter(iterable)
    last = next(it)
    for val in it:
        yield last, False
        last = val
    yield last, True