import os
import discord
import secrets
from commands.commands import Command
from util.undoers import get_simple_delete_undoer

floppas = []
_undo, _log = get_simple_delete_undoer('floppa')


def _init():
    for floppa in os.listdir('assets/floppas'):
        if 'floppa' not in floppa:
            continue

        floppas.append(floppa)


async def _handle(_, channel: discord.TextChannel, ___, m):
    with open('assets/floppas/' + secrets.choice(floppas), 'rb') as file:
        _log(await channel.send(file=discord.File(file, 'floppa.jpg')), m)


floppa_cmd = Command(_handle, ['floppa'],
                     'Return a random Floppa image (myokan)',
                     init_executor=_init, undo_executor=_undo)
