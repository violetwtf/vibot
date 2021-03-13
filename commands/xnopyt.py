import discord
from commands.commands import Command
from util.undoers import get_simple_delete_undoer

_undo, _log = get_simple_delete_undoer('xnopyt')


async def _handle(_, channel: discord.TextChannel, ___, m):
    _log(await channel.send('https://www.youtube.com/watch?v=aMgCBYgVwsI'), m)


xnopyt_cmd = Command(_handle, ['xnopyt'], 'xnopyt (rin)', undo_executor=_undo)
