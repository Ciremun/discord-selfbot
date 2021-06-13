import os
import asyncio
from os.path import join, dirname

from dotenv import load_dotenv

from src.client import QueueThread

if __name__ == '__main__':
    load_dotenv(join(dirname(__name__), '.env'))
    threads = []
    for token in os.environ.get('DISCORD_SELFBOT_TOKENS').split(';'):
        thread = QueueThread(daemon=True)
        thread.create_task(thread.run_client, token, bot=False)
        threads.append(thread)
    loop = asyncio.new_event_loop()
    loop.run_forever()
