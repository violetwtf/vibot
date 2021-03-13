from typing import Dict, List
from time import time


class Command:
    executor = None
    can_run_executor = None
    init_executor = None
    undo_executor = None
    aliases: List[str]
    description: str

    def __init__(self, executor, aliases: List[str], description: str,
                 can_run_executor=None, init_executor=None,
                 undo_executor=None):
        self.executor = executor
        self.can_run_executor = can_run_executor
        self.init_executor = init_executor
        self.undo_executor = undo_executor
        self.aliases = aliases
        self.description = description


commands: Dict[str, Command] = {}


def register(command: Command):
    if command.init_executor:
        start = time()
        command.init_executor()
        print(f'{command.aliases[0]} init done in {round((time() - start) * 1000, 5)}ms')

    for alias in command.aliases:
        commands[alias] = command
