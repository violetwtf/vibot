import discord
from typing import List
from util.args import read_string
from commands.commands import Command
from util.undoers import get_simple_delete_undoer

CODE_HEADER = '```py\n'
_undo, _log = get_simple_delete_undoer('eval')


async def _can_run(author: discord.User, _, __):
    if author.id != 294847443214794753:
        return 'You are not Violet.'
    return None


async def _handle(args: List[str], channel: discord.TextChannel,
                  author: discord.User, message: discord.Message):
    code = read_string(args, True)[0]

    # Remove "```py"
    if code[:len(CODE_HEADER)] == CODE_HEADER:
        code = code[len(CODE_HEADER):].strip()

    # Remove trailing "```"
    if code[-3:] == '```':
        code = code[:-3]

    # https://stackoverflow.com/a/53255739
    # Put it here to inherit scope
    # Make an async function with the code and `exec` it
    exec('async def __ex(): ' +
         ''.join(f'\n {line}' for line in code.split('\n')),
         locals())

    res = None
    res_title = 'Result:'

    # Reason: It's an eval. You cannot get less broad.
    # noinspection PyBroadException
    try:
        res = str(await locals()['__ex']())
    except Exception as e:
        res = str(e)
        res_title = '**OBJECTION!**'

    _log(await channel.send(res_title + ' ```py\n' + res + '```'), message)

eval_cmd = Command(_handle, ['eval'], 'Evaluates a line of code', _can_run,
                   undo_executor=_undo)
