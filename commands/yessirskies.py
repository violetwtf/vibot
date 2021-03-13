import discord
from commands.commands import Command
import random
from util.undoers import get_simple_delete_undoer

_undo, _log = get_simple_delete_undoer('yessirskies')


async def _handle(_, channel: discord.TextChannel, ___, m):
    msg = 'paul is stupid' if random.randrange(100) == 69 else 'yessirskies'
    _log(await channel.send(msg), m)


yessirskies_cmd = Command(_handle, ['yessirskies'], 'yessirskies (PaulBGD)',
                          undo_executor=_undo)
