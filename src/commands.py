import discord 

commands = {}

def command(*, name: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            return await func(*args, *kwargs)
        commands[name] = wrapper
        return wrapper
    return decorator

@command(name='avatar')
async def avatar_command(message: discord.Message):
    for user in message.mentions:
        await message.channel.send(user.avatar_url)