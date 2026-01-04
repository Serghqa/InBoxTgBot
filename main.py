import asyncio
import dialogs
import logging

from aiogram import Dispatcher, Router
from aiogram_dialog import setup_dialogs

from common import bot, set_bot_commands, engine, Session
from middleware import LoggingMiddleware, DbSessionMiddleware
from logging_setting import logging_config, setting_logging


setting_logging(logging_config)
logger = logging.getLogger(__name__)


def setup_all_dialogs(router: Router) -> Router:

    router.include_routers(*dialogs.routers)

    return router


def setting_dispatcher(dispatcher: Dispatcher) -> None:

    dispatcher.update.middleware(DbSessionMiddleware(Session))

    router = Router()

    router: Router = setup_all_dialogs(router)
    router.callback_query.middleware(LoggingMiddleware())
    router.message.middleware(LoggingMiddleware())

    dispatcher.include_router(router)
    setup_dialogs(dispatcher)


dp = Dispatcher()
setting_dispatcher(dispatcher=dp)


async def main():

    await set_bot_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
