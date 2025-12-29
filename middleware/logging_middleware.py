import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities.context import Context
from typing import Callable, Awaitable, Dict, Any


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        dialog_manager: DialogManager = data.get("dialog_manager")

        result = await handler(event, data)

        if dialog_manager:
            if dialog_manager.has_context():
                context: Context = dialog_manager.current_context()

                logger.info(
                    "\n**********\n"
                    "START_DATA=%s\n"
                    "DIALOG_DATA=%s\n"
                    "WIDGET_DATA=%s\n"
                    "STATE=%s\n"
                    "\n**********\n",
                    context.start_data,
                    context.dialog_data,
                    context.widget_data,
                    context.state,
                )

        return result
