import discord
import requests
from commands.commands import Command
from util.undoers import get_simple_delete_undoer

_undo, _log = get_simple_delete_undoer('chris')


async def _can_run(_, __, channel: discord.TextChannel):
    if not channel.nsfw:
        return 'This can only be run in an NSFW channel.'

    return None


async def _handle(_, channel: discord.TextChannel, ___, m):
    resp = requests.get('https://yiff.rest/v2/chris',
                        headers={'User-Agent': 'vibot'}).json()
    _log(await channel.send(resp['images'][0]['shortURL']), m)


chris_cmd = Command(_handle, ['chris'],
                    'Random Chris OOC message (August/Chris)',
                    _can_run, undo_executor=_undo)
