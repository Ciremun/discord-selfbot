import re
import io
from typing import Optional

import discord
import requests

from .utils import send_error, unicode_emojis
from .client import client
from .log import logger

try:
    import cairosvg
except OSError as e:
    logger.exception(e)

discord_emoji_re = re.compile(r'<a?:(\w+|\d+):(\d{18})>')
size_re = re.compile(r'size=(\d+)')
unusual_char_re = re.compile(r'[^\w\s,]')
commands = {}

def command(*, name: str):
    def decorator(func):
        async def wrapper(message: discord.Message):
            try:
                return await func(message)
            except Exception as e:
                await send_error(f'error: {e}', message, delay=3)
        commands[name] = wrapper
        return wrapper
    return decorator

@command(name='avatar')
async def avatar_command(message: discord.Message) -> Optional[str]:
    message_split = message.content.split(' ')[1:]
    size = None
    for part in message_split:
        if match := re.match(size_re, part):
            size = match.group(1)
    async def send_avatar(avatar_url: discord.Asset) -> str:
        avatar_url = str(avatar_url)
        if size:
            avatar_url = re.sub(size_re, f'size={size}', avatar_url)
        return avatar_url
    for user in message.mentions:
        return await send_avatar(user.avatar_url)
    for user_id in message_split:
        try:
            user_id = int(user_id)
        except Exception:
            continue
        if user := client.get_user(user_id):
            return await send_avatar(user.avatar_url)
        else:
            await send_error(f'id {user_id} not found', message, delay=3)

@command(name='exec')
async def exec_command(message: discord.Message):
    code = '\n'.join(message.content.split('\n')[2:])[:-3]
    if code:
        exec(code)

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
        await send_error(f'emoji {emoji_name} not found', message, delay=3)

@command(name='wrap')
async def wrap_command(message: discord.Message) -> str:
    message_split = message.content.split(" ")
    wrap_chars = message_split[1]
    inside = " ".join(message_split[2:])
    return f'{wrap_chars}{inside}{wrap_chars[::-1]}'

@command(name='eval')
async def eval_command(message: discord.Message):
    return eval(" ".join(message.content.split(' ')[1:]))

@command(name='replace')
async def replace_command(message: discord.Message) -> str:
    parts = message.content.split(' ')
    pattern = parts[1]
    repl = parts[2]
    here = " ".join(parts[3:])
    return re.sub(pattern, repl, here)

@command(name='upload')
async def upload(message: discord.Message):
    parts = message.content.split(' ')
    guild_name = parts[1]
    # TODO: use discord.utils.find with guild_name.lower()
    guild = discord.utils.get(client.guilds, name=guild_name)
    assert guild is not None
    emoji_name = parts[2]
    assert 2 <= len(emoji_name) <= 32
    emoji_url = parts[3]
    image = requests.get(emoji_url).content
    await guild.create_custom_emoji(name=emoji_name, image=image)

