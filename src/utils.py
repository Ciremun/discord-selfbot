from typing import Optional

import discord

async def send_error(error_message: str, message: discord.Message, *, delay: Optional[float] = None):
    message = await message.channel.send(error_message)
    await message.delete(delay=delay)