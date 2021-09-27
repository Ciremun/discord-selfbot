import re

import discord

import src.commands as c
from .utils import lookahead, send_error

clients = []
eval_re = re.compile(r'(\\?\$[^ \$]*)')


class Client(discord.Client):

    def __init__(self, **options) -> None:
        super().__init__()
        self.prefix = '$$'
        self.check_self = True
        self.convert_emoji_names_to_links = True
        for option, value in options.items():
            setattr(self, option, value)
        clients.append(self)

    async def on_ready(self) -> None:
        print(
            f'discord-selfbot [{self.user.name}#{self.user.discriminator}] is running ᕕ Pepega ᕗ')

    async def on_message(self, message: discord.Message) -> None:
        if (not self.check_self or message.author.id == self.user.id):
            if message.content.startswith(self.prefix):
                try:
                    pipe = message.content.split('|')
                    result = ''
                    begin = True
                    for command, end in lookahead(pipe):
                        command = command.strip()
                        if begin:
                            command = command[len(self.prefix):]
                            begin = False
                        if matches := re.finditer(eval_re, command):
                            offset = 0
                            for m in matches:
                                match = m.group(0)
                                if match[0] == '\\':
                                    s = m.start() - offset
                                    command = command[:s] + command[1 + s:]
                                    offset += 1
                                    continue
                                if match[1:]:
                                    command = command.replace(
                                    match, str(eval(match[1:])), 1)
                        message.content = f'{command} {result}'.strip()
                        message_split = command.split(' ')
                        command_func = c.commands[message_split[0]]
                        result = await command_func(message, self)
                        if end and result is not None:
                            await message.channel.send(result)
                except Exception as e:
                    await send_error(f'error: {e}', message)
                finally:
                    try:
                        await message.delete()
                    except Exception:
                        pass
            elif self.convert_emoji_names_to_links:
                try:
                    message_split = message.content.split(' ')
                    links = []
                    for part in message_split:
                        for emoji in self.emojis:
                            if part == emoji.name:
                                links.append(str(emoji.url))
                                break
                    if links:
                        if len(message_split) > 1:
                            message.content += '\n' + '\n'.join(links)
                        else:
                            message.content = links[0]
                        await message.edit(content=message.content)
                except Exception as e:
                    await send_error(f'error: {e}', message)
