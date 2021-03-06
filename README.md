# discord-selfbot

## Install

[Python 3](https://www.python.org/)

### env

|      Key        | Type  |                Value                     |
|-----------------|-------|------------------------------------------|
| `DISCORD_TOKEN` | `str` | discord authentication token (no prefix) |

### config.py

|     Var       |  Type  |          Description           |
|---------------|--------|--------------------------------|
| `prefix`      | `str`  | bot command prefix             |
| `bot`         | `bool` | user or bot token?             |
| `check_self`  | `bool` | can other users run commands?  |

## commands

pipe `|` is supported

|   cmd     |                  args                     |                                          description                                    |
|-----------|-------------------------------------------|-----------------------------------------------------------------------------------------|
| `avatar`  | `<mentions/ids> [size]`                   | get user avatar link                                                                    |
| `emoji`   | `<emoji name / emoji> [size]`             | get emoji link                                                                          |
| `wrap`    | `<chars> <string>`                        | wrap string in characters, end chars are reversed                                       |
| `exec`    | `code block`                              | execute  Python code                                                                    |
| `eval`    | `code line`                               | evaluate Python code                                                                    |
| `replace` | `<regex target> <regex replace> <string>` | replace characters in string using regular expressions                                  |
| `upload`  | `<guild name> <emoji name> <image url>`   | upload emoji via link                                                                   |
| `remind`  | `<timecode> <note>`                       | notify self with message `note` after `timecode` seconds `10:00 = 600s`                 |
| `weather` | `<location>`                              | get weather data for location                                                           |
| `echo`    | `<message["'%s]> [repl %s with]`          | return [formatted] message, fmt usage: `echo "hello %s world" uwu` -> `hello uwu world` |
| `loop`    | `<times> <cmd name> <cmd args>`           | run command N times                                                                     |