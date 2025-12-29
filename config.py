from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class InboxConfig:
    inbox_password: str
    user_name: str
    mail_server: str
    yandex_server: str


@dataclass
class Config:
    inbox: InboxConfig
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        inbox=InboxConfig(
            inbox_password=env("INBOX_PASSWORD"),
            user_name=env("USER_NAME"),
            mail_server=env("MAIL_SERVER"),
            yandex_server=env("YANDEX_SERVER"),
        ),
        tg_bot=TgBot(
            token=env("TOKEN"),
        ),
    )
