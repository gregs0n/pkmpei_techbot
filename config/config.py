# - *- coding: utf- 8 - *-
import configparser
from dataclasses import dataclass

@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    RATE_LIMIT: float
    PATH_DATABASE: str
    PATH_LOGS: str
    ADMINS: list[int]


def load_config(path: str) -> Config:
    read_config = configparser.ConfigParser()
    read_config.read(path)

    BOT_TOKEN = read_config['settings']['token'].strip()
    RATE_LIMIT = float(read_config['settings']['rate_limit'].strip())
    PATH_DATABASE = 'data/database.db'
    PATH_LOGS = 'data/updates.log'
    
    admins = read_config['settings']['admin_id'].strip()
    admins = admins.replace(' ', '')

    admins = admins.split(',')
    admins = list(map(int, admins))
    
    cnf = Config(
        tg_bot=TgBot(token=BOT_TOKEN),
        RATE_LIMIT=RATE_LIMIT,
        PATH_DATABASE=PATH_DATABASE,
        PATH_LOGS=PATH_LOGS,
        ADMINS=admins
    )
    
    return cnf
