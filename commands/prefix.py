import discord
from typing import List, Dict
from util import args as args_util
from context import get_db
from guild.settings import create_guild_if_not_exists, update_guild, \
    get_settings
from commands.commands import Command


last_prefixes: Dict[int, str] = {}


async def _can_run(author: discord.User, guild: discord.Guild, ___):
    if (await guild.fetch_member(author.id)).guild_permissions.manage_guild:
        return None
    return 'You need the **Manage Server** permission to do this.'


async def _undo(channel: discord.TextChannel, __, ___, guild_id: int, _____):
    prefix = last_prefixes[guild_id]
    await get_db().execute(
        'UPDATE guild_settings SET prefix = $1 WHERE id = $2',
        None if prefix == '' else prefix, guild_id)
    await update_guild(guild_id)
    await channel.send('Reverted prefix to **' +
                       ('(none)' if prefix == '' else prefix) +
                       '**')


async def _handle(args: List[str], channel: discord.TextChannel, ___, ____):
    prefix = args_util.read_string(args, True)[0]

    if not prefix:
        return

    guild: discord.Guild = channel.guild

    last_prefixes[guild.id] = get_settings(guild.id).prefix
    await create_guild_if_not_exists(guild.id)
    await get_db().execute(
        'UPDATE guild_settings SET prefix = $1 WHERE id = $2',
        prefix, guild.id)
    await update_guild(guild.id)

    await channel.send(f'Updated server prefix to: **{prefix}**.')

prefix_cmd = Command(_handle, ['prefix'], 'Set the prefix for your server',
                     _can_run, undo_executor=_undo)
