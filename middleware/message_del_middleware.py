import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from typing import Callable, Awaitable, Dict, Any


logger = logging.getLogger(__name__)


class MessageDeleterMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        result = await handler(event, data)
        if isinstance(event, Message) and not event.from_user.is_bot:
            try:
                await event.delete()
            except Exception:
                pass

        return result
