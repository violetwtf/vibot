import discord
import requests
from commands.commands import Command
from util.undoers import get_simple_delete_undoer

_undo, _log = get_simple_delete_undoer('cat')


async def _handle(_, channel: discord.TextChannel, ___, message: discord.Message):
    resp = requests.get('https://api.thecatapi.com/v1/images/search').json()
    _log(await channel.send(resp[0]['url']), message)

cat_cmd = Command(_handle, ['cat', 'catimage', 'catimg'],
                  'Return a random picture of a cat (Isabel)',
                  undo_executor=_undo)
