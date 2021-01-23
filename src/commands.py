from discord import Message
from .client import client

commands = {}

def command(*, name: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            return await func(*args, *kwargs)
        commands[name] = wrapper
        return wrapper
    return decorator

@command(name='avatar')
async def avatar_command(message: Message):
    for user in message.mentions:
        await message.channel.send(user.avatar_url)
    for user_id in message.content.split(' ')[1:]:
        try:
            user_id = int(user_id)
        except Exception:
            continue
        if user := client.get_user(user_id):
            await message.channel.send(user.avatar_url)

@command(name='exec')
async def exec_command(message: Message):
    try:
        code = '\n'.join(message.content.split('\n')[2:])[:-3]
        exec(code)
    except Exception as e:
        await message.channel.send(f'{e}')