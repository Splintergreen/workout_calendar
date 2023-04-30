from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()


@dataclass
class BotToken:
    token: str


@dataclass
class Config:
    bot_token: BotToken


def load_config() -> Config:
    token = os.getenv('TG_TOKEN')
    return Config(bot_token=BotToken(token))
