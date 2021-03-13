import json
import asyncpg
import discord
from config import Config
from context import client, set_config, set_db, get_config
from guild.settings import whitelist, load_settings as load_guild_settings

# Handlers
from handlers.message import on_message

# Commands
from commands import commands
from commands.seven_ball import seven_ball_cmd  # 7ball
from commands.cat import cat_cmd
from commands.chris import chris_cmd
from commands.dino_fact import dino_fact_cmd
from commands.eval import eval_cmd
from commands.floppa import floppa_cmd
from commands.fortune import fortune_cmd
from commands.help import help_cmd
from commands.ping import ping_cmd
from commands.prefix import prefix_cmd
from commands.random_color import random_color_cmd
from commands.toggle_random_color import toggle_random_color_cmd
from commands.undo import undo_cmd
from commands.violet_markov import violet_markov_cmd
from commands.xnopyt import xnopyt_cmd
from commands.yessirskies import yessirskies_cmd


def main():
    config = load_config()

    if config.debug:
        print('!!! WARNING: DEBUG ENABLED !!!\nPRESS ENTER TO CONFIRM STARTUP')
        input()
        print('Continuing with startup')

    set_config(config)

    client.event(on_message)

    # Register commands
    commands.register(seven_ball_cmd)  # 7ball
    commands.register(cat_cmd)
    commands.register(chris_cmd)
    commands.register(dino_fact_cmd)
    commands.register(eval_cmd)
    commands.register(floppa_cmd)
    commands.register(fortune_cmd)
    commands.register(help_cmd)
    commands.register(ping_cmd)
    commands.register(prefix_cmd)
    commands.register(random_color_cmd)
    commands.register(toggle_random_color_cmd)
    commands.register(undo_cmd)
    commands.register(violet_markov_cmd)
    commands.register(xnopyt_cmd)
    commands.register(yessirskies_cmd)

    # Run this last
    client.run(config.token)


@client.event
async def on_ready():
    config = get_config()
    db = await asyncpg.connect(host=config.db_host, port=config.db_port,
                               user=config.db_username,
                               password=config.db_password,
                               database=config.db_name)
    set_db(db)
    await load_guild_settings()
    print('Ready!')

    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game('@vibot help'))

    for guild in client.guilds:
        guild: discord.Guild = guild
        if config.whitelist and guild.id not in whitelist:
            await guild.leave()


@client.event
async def on_guild_join(guild: discord.Guild):
    if get_config().whitelist and guild.id not in whitelist:
        await guild.leave()


def load_config() -> Config:
    with open('config.json', 'r') as config_file:
        return Config(json.load(config_file))


if __name__ == "__main__":
    main()
