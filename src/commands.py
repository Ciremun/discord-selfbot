import re

import discord

from .utils import send_error
from .client import client

discord_emoji_re = re.compile(r'<a?:(\w+|\d+):(\d{18})>')
size_re = re.compile(r'size=(\d+)')
commands = {}

def command(*, name: str):
    def decorator(func):
        async def wrapper(message: discord.Message):
            try:
                await func(message)
            except Exception as e:
                await send_error(f'error: {e}', message, delay=3)
            await message.delete()
        commands[name] = wrapper
        return wrapper
    return decorator

@command(name='avatar')
async def avatar_command(message: discord.Message):
    message_split = message.content.split(' ')[1:]
    size = None
    for part in message_split:
        if match := re.match(size_re, part):
            size = match.group(1)
    async def send_avatar(avatar_url: discord.Asset):
        avatar_url = str(avatar_url)
        if size:
            avatar_url = re.sub(size_re, f'size={size}', avatar_url)
        await message.channel.send(avatar_url)
    for user in message.mentions:
        await send_avatar(user.avatar_url)
    for user_id in message_split:
        try:
            user_id = int(user_id)
        except Exception:
            continue
        if user := client.get_user(user_id):
            await send_avatar(user.avatar_url)
        else:
            await send_error(f'id {user_id} not found', message, delay=3)

@command(name='exec')
async def exec_command(message: discord.Message):
    code = '\n'.join(message.content.split('\n')[2:])[:-3]
    if code:
        exec(code)

@command(name='emoji')
async def emoji_command(message: discord.Message):
    message_split = message.content.split(' ')
    emoji_name = message_split[1]
    async def send_emoji_link(emoji: discord.Emoji):
        end = 'gif' if emoji.animated else 'png'
        size = '' if len(message_split) < 3 else f'?size={message_split[2]}'
        await message.channel.send(f'https://cdn.discordapp.com/emojis/{emoji.id}.{end}{size}')
    if emoji_id := re.search(discord_emoji_re, emoji_name):
        if emoji := client.get_emoji(int(emoji_id.group(2))):
            await send_emoji_link(emoji)
    elif emoji := discord.utils.get([e for g in client.guilds for e in g.emojis], name=emoji_name):
        await send_emoji_link(emoji)
    else:
        await send_error(f'emoji {emoji_name} not found', message, delay=3)