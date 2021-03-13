import discord
import secrets
from commands.commands import Command
from typing import Dict, List
from datetime import datetime, timedelta
from context import get_db


fortunes: List[str] = []
cache: Dict[int, datetime] = {}


def _init():
    with open('assets/fortune.txt') as fortune_file:
        global fortunes
        fortunes = fortune_file.read().splitlines()


async def _can_run(user: discord.User, __, ___):
    last_use = datetime.now() - timedelta(days=69)
    db_last_use = None
    db = get_db()

    if user.id in cache:
        last_use = cache[user.id]
    else:
        db_last_use = await db.fetchval(
            'SELECT last_use FROM fortune_usages WHERE id = $1', user.id)

        if db_last_use:
            last_use = db_last_use
            cache[user.id] = last_use

    can_use_again = last_use + timedelta(days=1)
    now = datetime.now()

    if can_use_again > now:
        return 'You can\'t use this for another ' + str(can_use_again - now)
    elif user.id in cache:
        del cache[user.id]

    if db_last_use:
        await db.execute('DELETE FROM fortune_usages WHERE id = $1', user.id)

    return None


async def _handle(_, channel: discord.TextChannel, user: discord.User, ____):
    await get_db().execute('INSERT INTO fortune_usages VALUES ($1, $2)',
                           user.id, datetime.now())

    await channel.send(':fortune_cookie: **Your fortune:** ' +
                       secrets.choice(fortunes))


fortune_cmd = Command(_handle, ['fortune', 'fortunecookie'],
                      'Read your fortune (julseejules)', _can_run, _init)
