from typing import Dict, List
from context import get_config
import discord
import secrets
from commands.commands import Command
from util.undoers import get_simple_delete_undoer

dinos: List[Dict[str, str]] = []
_undo, _log = get_simple_delete_undoer('dinofact')


def _init():
    with open('./assets/dinos.txt') as file:
        for line in file:
            if ' - ' not in line:
                continue

            parts = line.split(' - ')
            name = parts[0].strip()
            fact = parts[1].strip()

            dinos.append({'name': name, 'fact': fact})
            if get_config().debug:
                print('Loaded dino ' + name + ' - ' + fact)


async def _handle(_, channel: discord.TextChannel, ___, m):
    dino = secrets.choice(dinos)
    _log(await channel.send(f'🦕**{dino["name"]}** - {dino["fact"]}'), m)

dino_fact_cmd = Command(_handle, ['dinofact', 'dinofacts', 'dinofax'],
                        'Give a random dino fact! (Maisy)',
                        init_executor=_init, undo_executor=_undo)
