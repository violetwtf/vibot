import discord
from guild import settings
from context import client, get_config, undos
from commands.commands import commands


async def on_message(message: discord.Message):
    if message.author.bot:
        return

    guild: discord.Guild = message.guild
    prefix = settings.get_settings(guild.id).prefix

    prefixes = ['<@!' + str(client.user.id) + '> ']

    if get_config().debug:
        prefixes.append('!')

    if prefix != '':
        prefixes.append(prefix)

    prefixed = False

    for prefix in prefixes:
        content = message.content
        prefix_len = len(prefix)

        if content[:prefix_len] == prefix:
            prefixed = True
            parts = content[prefix_len:].split(' ')
            command_label = parts[0]

            if command_label in commands:
                command = commands[command_label]

                # If there's no executor requirement, we instantly bypass
                can_run_executor = not command.can_run_executor
                author = message.author

                if not can_run_executor:
                    # Run it
                    can_run_executor = await command.can_run_executor(
                        author,
                        guild,
                        message.channel)

                    if can_run_executor:
                        await message.channel.send('**Error:** ' +
                                                   can_run_executor)
                        return
                    else:
                        can_run_executor = True

                if can_run_executor:
                    args = parts[1:]
                    await command.executor(args, message.channel, author,
                                           message)

                    undos[author.id] = (command.aliases[0], args, guild.id,
                                        message.channel.id)
            break

    if not prefixed and message.author.id == 294847443214794753:
        with open('assets/violet.txt', 'a') as violet_file:
            violet_file.write('\n' + message.clean_content)
