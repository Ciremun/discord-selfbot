import json
from typing import Optional, Iterable, Tuple

import discord

unicode_emojis = json.load(open('emojis.json', encoding='utf-8'))
usage = {
    'avatar':    '<mentions/ids> [size] - get user avatar link',
    'emoji':     '<emoji name / emoji> [size] - get emoji link',
    'wrap':      '<chars> <string> - wrap string in characters, end chars are reversed',
    'exec':      'code block - execute  Python code',
    'eval':      'code line - evaluate Python code',
    'replace':   '<regex target> <regex replace> <string> - replace characters in string using regular expressions',
    'upload':    '<guild name> <emoji name> <image url> - upload emoji via link',
    'remind':    "<timecode> <note> - notify self with message 'note' after 'timecode' seconds '10:00 = 600s'",
    'weather':   '<location> - get weather data for location',
    'echo':      '<message' + '["' + "'%s]>" + "[repl %s with] - return [formatted] message, fmt usage: 'echo " + '"hello %s world"' + "uwu' -> 'hello uwu world'",
    'loop':      '<times> <cmd name> <cmd args> - run command N times',
    'help':      '[cmd] - get commands list/usage',
    'colorinfo': '<#hex or rgb> - get color image, rgb, hex',
    'animate':   '[cycles=1] [frame delay=1.0] <emojis> - animate emojis with message edit'
}


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


def hex3_to_hex6(hex_color: str) -> str:
    hex6 = '#'
    for h in hex_color.lstrip('#'):
        hex6 += f'{h}{h}'
    return hex6


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return '#%02x%02x%02x' % (r, g, b)


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i: i + 2], 16) for i in (0, 2, 4))
