import json
from typing import Optional, Iterable

import discord

unicode_emojis = json.load(open('emojis.json', encoding='utf-8'))

async def send_error(error_message: str, message: discord.Message, *, delay: Optional[float] = 3):
    message = await message.channel.send(error_message)
    await message.delete(delay=delay)

def lookahead(iterable: Iterable):
    it = iter(iterable)
    last = next(it)
    for val in it:
        yield last, False
        last = val
    yield last, True

def find_item(name: str, items: Iterable):
    name = name.lower()
    return discord.utils.find(lambda x: x.name.lower() == name, items)

def timecode_convert(timecode: str) -> int:
    """Get Seconds from timecode."""
    timecode = timecode.split(':')
    if len(timecode) == 1:
        return int(timecode[0])
    elif len(timecode) == 2:
        m, s = timecode[0], timecode[1]
        return int(m) * 60 + int(s)
    elif len(timecode) == 3:
        h, m, s = timecode[0], timecode[1], timecode[2]
        return int(h) * 3600 + int(m) * 60 + int(s)