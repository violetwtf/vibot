import discord
from context import client, get_db
from guild.settings import get_settings, update_guild, create_guild_if_not_exists
from commands.commands import Command


async def _can_run(user: discord.User, guild: discord.Guild, ___):
    member = await guild.fetch_member(user.id)
    self_member = await guild.fetch_member(client.user.id)

    if not member.guild_permissions.manage_guild:
        return 'You need the **Manage Server** permission to do this.'
    elif not self_member.guild_permissions.manage_roles:
        return 'I need the **Manage Roles** permission to do this.'

    return None


async def _undo(channel: discord.TextChannel, __, ___, guild_id: int, _____):
    guild: discord.Guild = channel.guild

    if guild.id != guild_id:
        await channel.send('You didn\'t run that command here!')
        return

    new = not get_settings(guild_id).random_color_enabled
    await get_db().execute(
        'UPDATE guild_settings SET random_color_enabled = $1 WHERE id = $2',
        new, guild_id)
    await update_guild(guild_id)

    await channel.send('Reverted random colors to **' +
                       ('enabled' if new else 'disabled') +
                       '**.')


async def _handle(_, channel: discord.TextChannel, ___, ____):
    guild_id = channel.guild.id
    new = not get_settings(guild_id).random_color_enabled

    await create_guild_if_not_exists(guild_id)
    await get_db().execute(
        'UPDATE guild_settings SET random_color_enabled = $1 WHERE id = $2',
        new, guild_id)
    await update_guild(guild_id)

    await channel.send('**' +
                       ('Enabled' if new else 'Disabled') +
                       '** random colors.')


toggle_random_color_cmd = Command(_handle, ['togglerandomcolor'],
                                  'Enable/disable the random color command ' +
                                  'in your server. (Sandy)', _can_run,
                                  undo_executor=_undo)
