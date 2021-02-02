import discord

import src.config as cfg
import src.commands as c
from .log import logger
from .utils import lookahead, send_error

client = discord.Client()


@client.event
async def on_ready(*args, **kwargs):
    print('ᕕ Pepega ᕗ')


@client.event
async def on_message(message: discord.Message):
    if (not cfg.check_self or message.author.id == client.user.id) and message.content.startswith(cfg.prefix):
        try:
            pipe = message.content.split('|')
            result = ''
            begin = True
            for command, end in lookahead(pipe):
                command = command.strip()
                message.content = f'{command} {result}'.strip()
                message_split = command.split(' ')
                command_func = c.commands[message_split[0][len(cfg.prefix):]] if begin else c.commands[message_split[0]]
                result = await command_func(message)
                if end and result is not None:
                    await message.channel.send(result)
                begin = False
        except Exception as e:
            await send_error(f'error: {e}', message)
            logger.exception(e)
        finally:
            await message.delete()