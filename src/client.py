import discord

import src.config as cfg
import src.commands as c
from .log import logger

client = discord.Client()


@client.event
async def on_ready(*args, **kwargs):
    print('pepega is running')


@client.event
async def on_message(message: discord.Message):
    if message.author.id == client.user.id and message.content.startswith(cfg.prefix):
        try:
            await c.commands[message.content.split()[0][len(cfg.prefix):]](message)
        except Exception as e:
            logger.exception(e)