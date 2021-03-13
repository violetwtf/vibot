from typing import Dict, List
from context import get_db
import asyncpg


class GuildSettings:
    prefix: str
    random_color_enabled: bool
    commands_enabled: bool

    def __init__(self, prefix: str, random_color_enabled: bool = False):
        self.prefix = prefix
        self.random_color_enabled = random_color_enabled
        self.commands_enabled = True


default_settings = GuildSettings(prefix='')


async def load_settings():
    db = get_db()
    for guild in await db.fetch('SELECT * FROM guild_settings'):
        await update_guild_by_row(guild)
    for guild in await db.fetch('SELECT * FROM whitelist'):
        whitelist.append(guild['id'])


async def update_guild_by_row(row: asyncpg.Record):
    prefix = row['prefix']
    random_color_enabled = row['random_color_enabled']
    guild_settings[row['id']] = GuildSettings('' if not prefix else prefix,
                                              random_color_enabled)


async def update_guild(guild_id: int):
    await update_guild_by_row(await get_db().fetchrow(
        'SELECT * FROM guild_settings WHERE id = $1',
        guild_id))


async def create_guild_if_not_exists(guild_id: int):
    db = get_db()
    count = await db.fetchval(
        'SELECT COUNT(id) FROM guild_settings WHERE id = $1',
        guild_id)

    if count > 0:
        return

    await update_guild_by_row(await db.fetchrow(
        'INSERT INTO guild_settings (id) VALUES ($1) RETURNING *',
        guild_id))


def get_settings(guild_id: int):
    if guild_id in guild_settings:
        return guild_settings[guild_id]
    else:
        return default_settings


guild_settings: Dict[int, GuildSettings] = {}
whitelist: List[int] = []
