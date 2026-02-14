from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:

    TOKEN: str


@dataclass
class InboxConfig:

    MAIL_SERVER: str
    YANDEX_SERVER: str

    def get_ordered_servers(self) -> list[str]:

        return [
            self.MAIL_SERVER,
            self.YANDEX_SERVER,
        ]


@dataclass
class DbConfig:

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str


@dataclass
class SecretKey:

    SECRET_KEY: str


@dataclass
class Config:

    inbox: InboxConfig
    tg_bot: TgBot
    db: DbConfig
    secret_key: SecretKey


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        inbox=InboxConfig(
            MAIL_SERVER=env("MAIL_SERVER"),
            YANDEX_SERVER=env("YANDEX_SERVER"),
        ),
        tg_bot=TgBot(
            TOKEN=env("TOKEN"),
        ),
        db=DbConfig(
            DB_USER=env("POSTGRES_USER"),
            DB_PASSWORD=env("POSTGRES_PASSWORD"),
            DB_HOST=env("POSTGRES_HOST"),
            DB_NAME=env("POSTGRES_NAME"),
        ),
        secret_key=SecretKey(
            SECRET_KEY=env("SECRET_KEY"),
        ),
    )
