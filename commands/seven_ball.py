import discord
import secrets
from commands.commands import Command
from util.undoers import get_simple_delete_undoer

_undo, _log = get_simple_delete_undoer('7ball')

messages = [
    'i don\'t know... maybe?',
    'maybe',
    'try again in 10 minutes',
    'try again in 1 hour',
    'try again in 1 day',
    'ask again later',
    'try again later',
    'possibly',
    'potentially',
    'perhaps',
    'you might want to, you might not',
    'i\'m not quite sure',
    'ask me again',
    'i think that might be a great idea! ...or maybe not! try asking again',
]


async def _handle(_, channel: discord.TextChannel, ___, m):
    _log(await channel.send(':8ball: ' + secrets.choice(messages)), m)


seven_ball_cmd = Command(_handle, ['7ball'],
                         'Nothing wrong with this 8 ball... (Penple)',
                         undo_executor=_undo)
