import discord
from commands.commands import commands, Command
from context import undos


async def _can_run(user: discord.User, __, ___):
    if user.id not in undos:
        return 'You have no action to undo!'

    command = commands[undos[user.id][0]]
    name = command.aliases[0]

    if name == 'undo':
        return 'You can\'t undo an undo.'

    if not command.undo_executor:
        return f'`{name}` does not support undo.'

    return None


async def _handle(_, channel: discord.TextChannel, user: discord.User,
                  message: discord.Message):
    undo = undos[user.id]
    await commands[undo[0]].undo_executor(channel, user, undo[1], undo[2],
                                          undo[3])

    await message.delete()


undo_cmd = Command(_handle, ['undo', 'ohgodpleaseididntmeanto'],
                   'Undo your last command', _can_run)
