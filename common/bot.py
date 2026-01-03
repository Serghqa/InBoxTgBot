import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config import load_config, Config


logger = logging.getLogger(__name__)

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
    bot_name = await bot.get_my_name()
    bot_commands = await bot.get_my_commands()
    logger.info(
        "Бот %s создан. Командное меню = %s",
        bot_name.name, bot_commands
    )

bot = Bot(
    token=config.tg_bot.TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
