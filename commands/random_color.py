import discord
from guild.settings import get_settings
from commands.commands import Command
from context import client
from typing import Dict

PREFIX = 'vibot random color'


last_colors: Dict[int, discord.Color] = {}


def _color_to_hex(color: discord.Color) -> str:
    return '#%02x%02x%02x' % color.to_rgb()


async def _can_run(user: discord.User, guild: discord.Guild, ___):
    member = await guild.fetch_member(user.id)
    self_member = await guild.fetch_member(client.user.id)

    if not get_settings(guild.id).random_color_enabled:
        msg = 'Random color is not enabled in this server.'

        if member.guild_permissions.manage_guild:
            msg = msg + \
                  ' You can enable it using the **togglerandomcolor** command.'

        return msg
    elif not self_member.guild_permissions.manage_roles:
        return 'I need the **Manage Roles** permission to do this.'
    elif self_member.roles[-1].position < member.roles[-1].position:
        return 'Your role is higher than or equal to mine!'

    return None


async def _undo(channel: discord.TextChannel, user: discord.User, ___,
                guild_id: int, _____):
    color = last_colors[user.id]
    guild: discord.Guild = channel.guild

    if guild.id != guild_id:
        await channel.send('Your last random color was not in this server!')
        return

    member: discord.Member = await guild.fetch_member(user.id)

    role = None

    for r in member.roles:
        r: discord.Role = r
        if r.name[:len(PREFIX)] == PREFIX:
            role = r

    if not role:
        await channel.send('Your random color role no longer exists')
        return

    if color:
        await channel.send(f'Reverted color to **{_color_to_hex(color)}**!')
        await role.edit(color=color)
    else:
        await channel.send(f'Removed random color role!')
        await role.delete()


async def _handle(_, channel: discord.TextChannel, user: discord.User, ____):
    guild: discord.Guild = channel.guild

    member = await guild.fetch_member(user.id)
    self_member = await guild.fetch_member(client.user.id)

    role: discord.Role = None
    role_existed = False

    for r in member.roles:
        r: discord.Role = r  # For syntax highlighting
        if r.name[:len(PREFIX)] == PREFIX:
            role = r
            role_existed = True
            break
    if not role:
        role = await guild.create_role(reason=PREFIX)

    # Hey, what a handy function! Thanks, discord.py!
    color = discord.Color.random()
    hex_color = _color_to_hex(color)

    fields = {'name': PREFIX + ' (' + hex_color + ')', 'color': color,
              'permissions': discord.Permissions.none()}

    if not role_existed:
        fields['position'] = self_member.roles[-1].position - 1
        last_colors[user.id] = None
    else:
        last_colors[user.id] = role.color

    await role.edit(**fields)
    if not role_existed:
        await member.add_roles(role)
    await channel.send('Changed your color to **' + hex_color + '**!')


random_color_cmd = Command(_handle, ['randomcolor'],
                           'Give yourself a random color! (Sandy)', _can_run,
                           undo_executor=_undo)
