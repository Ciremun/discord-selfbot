import os
import asyncio

from dotenv import load_dotenv

from src.client import Client


async def main():
    load_dotenv()
    clients = []
    for token in os.environ.get('DISCORD_SELFBOT_TOKENS').split(';'):
        client = Client()
        client.loop.create_task(client.start(token, bot=False))
        clients.append(client)
    await asyncio.sleep(6969)

if __name__ == '__main__':
    asyncio.run(main())
