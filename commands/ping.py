import discord
from commands.commands import Command
from util.undoers import get_simple_delete_undoer

_undo, _log = get_simple_delete_undoer('ping')


async def _handle(_, channel: discord.TextChannel, __, m):
    _log(await channel.send('Pong!'), m)

ping_cmd = Command(_handle, ['ping'], 'Have the bot say "Pong!" back to you',
                   undo_executor=_undo)
