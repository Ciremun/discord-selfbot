import asyncio
import re
import io
from typing import Optional, Callable, Any

import discord
import requests

import src.config as cfg

from .utils import (
    send_error,
    unicode_emojis,
    find_item,
    timecode_convert
)
from .client import client
from .log import logger

try:
    import cairosvg
except OSError as e:
    logger.exception(e)

discord_emoji_re = re.compile(r'<a?:(\w+|\d+):(\d{18})>')
discord_avatar_size_re = re.compile(r'size=\d{1,4}$')
up_to_4_digits_re = re.compile(r'^\d{1,4}$')
unusual_char_re = re.compile(r'[^\w\s,]')
replace_re = re.compile(r'^[\"\']([^\"\']+)[\"\'] [\"\']([^\"\']+)[\"\'] (.*)$')
commands = {}

def command(*, name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        async def wrapper(message: discord.Message) -> Any:
            try:
                return await func(message)
            except Exception as e:
                await send_error(f'error: {e}', message)
        wrapper.__name__ = func.__name__
        commands[name] = wrapper
        return wrapper
    return decorator

@command(name='avatar')
async def avatar_command(message: discord.Message) -> str:
    message_split = message.content.split(' ')[1:]
    size = None
    for part in message_split:
        if match := re.match(up_to_4_digits_re, part):
            size = match.group(0)
            break
    async def send_avatar(avatar_url: discord.Asset) -> str:
        avatar_url = str(avatar_url)
        if size:
            avatar_url = re.sub(discord_avatar_size_re, f'size={size}', avatar_url)
        return avatar_url
    urls = []
    for user in message.mentions:
        urls.append(await send_avatar(user.avatar_url))
    for user_id in message_split:
        try:
            assert len(user_id) > 16
            user_id = int(user_id)
        except Exception:
            continue
        if user := client.get_user(user_id):
            urls.append(await send_avatar(user.avatar_url))
        else:
            await send_error(f'id {user_id} not found', message)
    return ' '.join(urls)

@command(name='exec')
async def exec_command(message: discord.Message) -> None:
    code = '\n'.join(message.content.split('\n')[2:])[:-3]
    if code:
        exec(code)

@command(name='eval')
async def eval_command(message: discord.Message) -> Any:
    return eval(' '.join(message.content.split(' ')[1:]))

@command(name='emoji')
async def emoji_command(message: discord.Message) -> Optional[str]:
    message_split = message.content.split(' ')
    emoji_name = message_split[1]
    async def send_emoji_link(emoji: discord.Emoji) -> str:
        size = '' if len(message_split) < 3 else f'?size={message_split[2]}'
        return f'{emoji.url}{size}'
    if emoji_id := re.search(discord_emoji_re, emoji_name):
        if emoji := client.get_emoji(int(emoji_id.group(2))):
            return await send_emoji_link(emoji)
    elif emoji := discord.utils.get(client.emojis, name=emoji_name):
        return await send_emoji_link(emoji)
    else:
        if re.match(unusual_char_re, emoji_name):
            for emoji in unicode_emojis:
                if emoji['emoji'] == emoji_name:
                    svg = requests.get(emoji['svg']).content
                    png = cairosvg.svg2png(svg)
                    await message.channel.send(file=discord.File(fp=io.BytesIO(png), filename='image.png'))
                    return
        await send_error(f'emoji {emoji_name} not found', message)

@command(name='wrap')
async def wrap_command(message: discord.Message) -> str:
    message_split = message.content.split(' ')
    wrap_chars = message_split[1]
    inside = ' '.join(message_split[2:])
    return f'{wrap_chars}{inside}{wrap_chars[::-1]}'

@command(name='replace')
async def replace_command(message: discord.Message) -> str:
    if match := re.match(replace_re, ' '.join(message.content.split(' ')[1:])):
        pattern = match.group(1)
        repl = match.group(2)
        here = match.group(3)
    else:
        parts = message.content.split(' ')
        pattern = parts[1]
        repl = parts[2]
        here = ' '.join(parts[3:])
    return re.sub(pattern, repl, here)

@command(name='upload')
async def upload_command(message: discord.Message) -> None:
    parts = message.content.split(' ')
    guild_name = parts[1]
    guild = find_item(guild_name, client.guilds)
    assert guild is not None
    emoji_name = parts[2]
    assert 2 <= len(emoji_name) <= 32
    emoji_url = parts[3]
    image = requests.get(emoji_url).content
    await guild.create_custom_emoji(name=emoji_name, image=image)

@command(name='remind')
async def remind_command(message: discord.Message) -> str:
    parts = message.content.split(' ')
    remind_in = timecode_convert(parts[1])
    note = ' '.join(parts[2:])
    async def reminder(remind_in: int, note: str) -> None:
        await asyncio.sleep(remind_in)
        await message.channel.send(f'{message.author.mention}, {note}')
    client.loop.create_task(reminder(remind_in, note))

@command(name='weather')
async def weather_command(message: discord.Message) -> str:
    parts = message.content.split(' ')
    location = ' '.join(parts[1:])
    url = cfg.weather_command_url.replace('%s', location)
    result = requests.get(url)
    return result.text