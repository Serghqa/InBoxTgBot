from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config import load_config, Config


config: Config = load_config()


async def set_bot_commands(bot: Bot):

    commands = [
        BotCommand(
            command="/start",
            description="Перезапустить бота",
        ),
        BotCommand(
            command="/update",
            description="Обновить",
        )
    ]

    await bot.set_my_commands(commands)

bot = Bot(
    token=config.tg_bot.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
