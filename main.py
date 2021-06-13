async def main():
    from dotenv import load_dotenv
    load_dotenv()
    from src.client import Client
    clients = []
    import os
    for token in os.environ.get('DISCORD_SELFBOT_TOKENS').split(';'):
        client = Client()
        client.loop.create_task(client.start(token, bot=False))
        clients.append(client)

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(main())
        loop.run_forever()
    finally:
        loop.close()
