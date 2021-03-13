from discord import Client
from config import Config
import asyncpg
from typing import Dict, List, Tuple

client = Client()
config: Config
db: asyncpg.Connection
# user id -> (command name, command args, guild id, channel id)
undos: Dict[int, Tuple[str, List[str], int, int]] = {}


def get_db():
    return db


def set_db(d: asyncpg.Connection):
    global db
    db = d


def get_config():
    return config


def set_config(conf: Config):
    global config
    config = conf
