from typing import Dict


class Config:
    token: str
    debug: bool

    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    def __init__(self, config_dict: Dict[str, any]):
        self.token = str(config_dict['token'])
        self.debug = bool(config_dict['debug'])

        self.db_username = str(config_dict['db_username'])
        self.db_password = str(config_dict['db_password'])
        self.db_host = str(config_dict['db_host'])
        self.db_port = int(config_dict['db_port'])
        self.db_name = str(config_dict['db_name'])
