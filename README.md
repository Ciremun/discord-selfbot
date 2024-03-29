# discord-selfbot

## Install

[Python 3](https://www.python.org/)

### env

|      Key                 | Type  |                Value                                     |
|--------------------------|-------|----------------------------------------------------------|
| `DISCORD_SELFBOT_TOKENS` | `str` | discord authentication tokens (no prefix, separator=`;`) |
| `BTTV_TOKEN`             | `str` | bttv token                                               |

### Client class options

|     Var                         |  Type  |          Description           |
|---------------------------------|--------|--------------------------------|
| `prefix`                        | `str`  | bot command prefix             |
| `check_self`                    | `bool` | can other users run commands?  |
| `convert_emoji_names_to_links`  | `bool` | convert emoji names to links?  |

## commands & misc

pipe `|` is supported  
eval in command string: `$$avatar $message.author.id`  
emoji names are converted to links by default

|   cmd          |                  args                     |                                          description                                    |
|----------------|-------------------------------------------|-----------------------------------------------------------------------------------------|
| `avatar`       | `<mentions/ids> [size]`                   | get user avatar link                                                                    |
| `emoji`        | `<emoji name / emoji> [size]`             | get emoji link                                                                          |
| `wrap`         | `<chars> <string>`                        | wrap string in characters, end chars are reversed                                       |
| `exec`         | `code block`                              | execute  Python code                                                                    |
| `eval`         | `code line`                               | evaluate Python code                                                                    |
| `replace`      | `<regex target> <regex replace> <string>` | replace characters in string using regular expressions                                  |
| `upload`       | `<guild name> <emoji name> <image url>`   | upload emoji via link                                                                   |
| `remind`       | `<timecode> <note>`                       | notify self with message `note` after `timecode` seconds `10:00 = 600s`                 |
| `weather`      | `<location>`                              | get weather data for location                                                           |
| `echo`         | `<message["'%s]> [repl %s with]`          | return [formatted] message, fmt usage: `echo "hello %s world" uwu` -> `hello uwu world` |
| `loop`         | `<times> <cmd name> <cmd args>`           | run command N times                                                                     |
| `help`         | `[cmd]`                                   | get commands list/usage                                                                 |
| `colorinfo`    | `<#hex or rgb>`                           | get color image, rgb, hex                                                               |
| `animate`      | `[cycles=1] [frame delay=1.0] <emojis>`   | animate emojis with message edit                                                        |
| `showcmd`      | `<command>`                               | get command source code                                                                 |
| `cfg`          | `<attr> [value]`                          | get / set Client class attribute                                                        |
| `bttv`         | `<query> [size: any(1x, 2x, 3x)]`         | get emote url from bttv search                                                          |
