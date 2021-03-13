import discord
from typing import Dict, Tuple
from context import client


# command name -> user id -> (guild id, channel id, command message id,
# response message id)
messages: Dict[str, Dict[int, Tuple[int, int, int, int]]] = {}


def get_simple_delete_undoer(command_name: str):
    messages[command_name] = {}

    async def _undo(_, user: discord.User, ___, ____, _____):
        undo = messages[command_name][user.id]
        guild: discord.Guild = await client.fetch_guild(undo[0])
        print(type(guild))
        channel: discord.TextChannel = client.get_channel(undo[1])
        print(undo[1])
        print(type(channel))
        command_message: discord.Message = await channel.fetch_message(undo[2])
        response_message: discord.Message = await channel.fetch_message(undo[3])

        await command_message.delete()
        await response_message.delete()

    def _log(response_message: discord.Message, command_message: discord.Message):
        messages[command_name][command_message.author.id] = (
            command_message.guild.id, command_message.channel.id,
            command_message.id, response_message.id)

    return _undo, _log
