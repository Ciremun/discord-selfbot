import asyncio
import re
import io
import os
import inspect
from functools import wraps
from typing import Optional, Callable, Any, List

import discord
import requests
from PIL import Image

from .utils import (
    send_error,
    find_item,
    unicode_emojis,
    timecode_convert,
    usage,
    hex3_to_hex6,
    hex_to_rgb,
    rgb_to_hex
)

discord_emoji_re = re.compile(r'<a?:(\w+|\d+):(\d{18})>')
discord_avatar_size_re = re.compile(r'size=\d{1,4}$')
up_to_4_digits_re = re.compile(r'^\d{1,4}$')
unusual_char_re = re.compile(r'[^\w\s,]')
replace_re = re.compile(
    r'^[\"\']([^\"\']+)[\"\'] [\"\']([^\"\']+)[\"\'] (.*)$')
echo_re = re.compile(r'^[\"\']([^\"\']+)[\"\'] (.*)$')
hex_color_regex = re.compile(r'^#([A-Fa-f0-9]{6})$')
hex3_color_regex = re.compile(r'^#([A-Fa-f0-9]{3})$')
rgb_regex = re.compile(r'^(?:(?:^|,?\s*)([01]?\d\d?|2[0-4]\d|25[0-5])){3}$')
rgb_hex_regex = re.compile(
    r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$|^(?:(?:^|,?\s*)([01]?\d\d?|2[0-4]\d|25[0-5])){3}$')
bttv_token = os.environ.get('BTTV_TOKEN')
commands = {}


def command(*, name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(message: discord.Message, client: discord.Client) -> Any:
            try:
                return await func(message, client)
            except Exception as e:
                await send_error(f'error: {e}', message)
        commands[name] = wrapper
        return wrapper
    return decorator


@command(name='avatar')
async def avatar_command(message: discord.Message, client: discord.Client) -> str:
    message_split = message.content.split(' ')[1:]
    size = None
    for part in message_split:
        if match := re.match(up_to_4_digits_re, part):
            size = match.group(0)
            break

    async def send_avatar(avatar_url: discord.Asset) -> str:
        avatar_url = str(avatar_url)
        if size:
            avatar_url = re.sub(discord_avatar_size_re,
                                f'size={size}', avatar_url)
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
async def exec_command(message: discord.Message, client: discord.Client) -> None:
    code = '\n'.join(message.content.split('\n')[2:])[:-3]
    if code:
        exec(code)


@command(name='eval')
async def eval_command(message: discord.Message, client: discord.Client) -> Any:
    return eval(' '.join(message.content.split(' ')[1:]))


@command(name='emoji')
async def emoji_command(message: discord.Message, client: discord.Client) -> Optional[str]:
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
                    return emoji['svg']
        await send_error(f'emoji {emoji_name} not found', message)


@command(name='wrap')
async def wrap_command(message: discord.Message, client: discord.Client) -> str:
    message_split = message.content.split(' ')
    wrap_chars = message_split[1]
    inside = ' '.join(message_split[2:])
    return f'{wrap_chars}{inside}{wrap_chars[::-1]}'


@command(name='replace')
async def replace_command(message: discord.Message, client: discord.Client) -> str:
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
async def upload_command(message: discord.Message, client: discord.Client) -> None:
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
async def remind_command(message: discord.Message, client: discord.Client) -> str:
    parts = message.content.split(' ')
    remind_in = timecode_convert(parts[1])
    note = ' '.join(parts[2:])

    async def reminder(remind_in: int, note: str) -> None:
        await asyncio.sleep(remind_in)
        await message.channel.send(f'{message.author.mention}, {note}')
    client.loop.create_task(reminder(remind_in, note))


@command(name='weather')
async def weather_command(message: discord.Message, client: discord.Client) -> str:
    parts = message.content.split(' ')
    location = ' '.join(parts[1:])
    url = 'https://wttr.in/%s?format=4'.replace('%s', location)
    result = requests.get(url)
    return result.text


@command(name='echo')
async def echo_command(message: discord.Message, client: discord.Client) -> str:
    parts = message.content.split(' ')
    args = ' '.join(parts[1:])
    if match := re.match(echo_re, args):
        result = match.group(1)
        repl = match.group(2)
        return result.replace('%s', repl)
    else:
        return args


@command(name='loop')
async def loop_command(message: discord.Message, client: discord.Client) -> None:
    parts = message.content.split(' ')
    cmd = parts[2]
    times = parts[1]
    args = ' '.join(parts[3:])
    for _ in range(int(times)):
        message.content = f'{client.prefix}{cmd} {args}'
        await client.on_message(message)


@command(name='help')
async def help_command(message: discord.Message, client: discord.Client) -> None:
    parts = message.content.split(' ')
    try:
        cmd = parts[1]
    except IndexError:
        await message.channel.send(f'commands: {", ".join(list(commands.keys()))}')
        return
    help_message = usage.get(cmd)
    if not help_message:
        raise KeyError(f"help for command `{cmd}` doesn't exist")
    await message.channel.send(f'{cmd}: {help_message}')


@command(name="colorinfo")
async def colorinfo_command(message: discord.Message, client: discord.Client) -> None:
    messagesplit = message.content.split()
    color_code = ' '.join(messagesplit[1:])
    if not color_code:
        await message.channel.send(f'{message.author.mention}, no color! usage: colorinfo <#hex or rgb>')
        return
    if not re.match(rgb_hex_regex, color_code):
        await message.channel.send(f'{message.author.mention}, color: #hex or rgb, example: #f542f2 or 245, 66, 242')
        return
    if re.match(rgb_regex, color_code):
        try:
            r, g, b = [int(i.strip(',')) for i in color_code.split()]
            color_code = rgb_to_hex(r, g, b)
        except ValueError:
            await message.channel.send(f'{message.author.mention}, rgb example: 245, 66, 242')
            return
    elif re.match(hex3_color_regex, color_code):
        color_code = hex3_to_hex6(color_code)
    color_img = Image.new("RGB", (100, 100), color_code)
    with io.BytesIO() as image_binary:
        color_img.save(image_binary, 'PNG')
        image_binary.seek(0)
        await message.channel.send(f'color: rgb{hex_to_rgb(color_code)}, {color_code}',
                                   file=discord.File(fp=image_binary, filename='color.png'))


@command(name="animate")
async def animate_command(message: discord.Message, client: discord.Client) -> None:
    if matches := re.findall(discord_emoji_re, message.content):
        if len(matches) < 2:
            await send_error("error: at least 2 emojis needed", message)
            return None
        message_parts: List[str] = message.content.split()
        cycles = int(message_parts[1]) if message_parts[1].isdigit() else 1
        frame_delay = 1.0
        try:
            frame_delay = float(message_parts[2])
        except Exception:
            pass
        for _ in range(cycles):
            for match in matches:
                emoji = client.get_emoji(int(match[1]))
                if emoji is None:
                    await send_error(f"error: couldn't get emoji '{match[0]}'")
                    return None
                await message.edit(content=emoji)
                await asyncio.sleep(frame_delay)
        return None
    await send_error("error: no emojis provided", message)
    return None

@command(name="showcmd")
async def showcmd_command(message: discord.Message, client: discord.Client) -> Optional[str]:
    message_parts = message.content.split()
    try:
        cmd = commands.get(message_parts[1], None)
        if cmd is None:
            await send_error(f"error: command '{message_parts[1]}' was not found", message)
            return None
    except IndexError:
        await send_error("error: no command provided", message)
        return None
    return f'```python\n{inspect.getsource(cmd)}```'

@command(name="cfg")
async def cfg_command(message: discord.Message, client: discord.Client) -> Optional[str]:
    message_parts = message.content.split()
    target = message_parts[1]
    try:
        value = eval(message_parts[2])
        setattr(client, target, value)
    except IndexError:
        return str(getattr(client, target))

@command(name="bttv")
async def bttv_command(message: discord.Message, client: discord.Client) -> None:
    message_parts = message.content.split()
    query = message_parts[1]
    response = requests.get(f'https://api.betterttv.net/3/emotes/shared/search?query={query}&offset=0&limit=1', headers={
        'authorization': f'Bearer {bttv_token}'
    })
    if response.status_code == 200:
        size = message_parts[2] if len(message_parts) == 3 else '2x'
        response_json = response.json()
        response = requests.get(f'https://cdn.betterttv.net/emote/{response_json[0]["id"]}/{size}')
        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            fmt = str(image.format) or 'PNG'
            with io.BytesIO() as output:
                image.save(output, format=fmt)
                filename = response_json[0].get("code") or 'emote'
                await message.channel.send(file=discord.File(output, filename=f'{filename}.{fmt.lower()}'))
            return
    await send_error(f'{response.status_code}: {response.text}', message)
