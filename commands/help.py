import discord
from commands.commands import commands, Command
from util.undoers import get_simple_delete_undoer

_undo, _log = get_simple_delete_undoer('help')


async def _handle(_, channel: discord.TextChannel, author: discord.User, m):
    helps = []
    seen = []

    for command in commands.values():
        if command in seen:
            continue

        seen.append(command)

        if command.can_run_executor:
            if await command.can_run_executor(author, channel.guild, channel):
                continue

        helps.append(f'**{command.aliases[0]}** - {command.description}')

    _log(await channel.send('\n'.join(helps)), m)


help_cmd = Command(_handle, ['help'], 'List all commands', undo_executor=_undo)
