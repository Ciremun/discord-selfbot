if __name__ == '__main__':
    import os
    from os.path import join, dirname
    from dotenv import load_dotenv

    import src.config
    import src.commands
    from src.client import client

    load_dotenv(join(dirname(__file__), '.env'))

    client.run(os.environ.get('DISCORD_TOKEN'), bot=src.config.bot)