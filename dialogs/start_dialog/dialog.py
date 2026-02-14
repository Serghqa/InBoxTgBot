import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import (
    Dialog,
    DialogManager,
    StartMode,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Jinja
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .handlers import (
    to_add_mail,
    to_select_mail,
)
from db.models import User
from db.services import UserDAO
from dialogs.states import StartSG


logger = logging.getLogger(__name__)

start_router = Router()


@start_router.message(F.text, CommandStart())
async def command_start(
    message: Message,
    dialog_manager: DialogManager
) -> None:

    session: AsyncSession = dialog_manager.middleware_data.get("db_session")
    user_id: int = dialog_manager.event.from_user.id
    user_dao = UserDAO(
        session=session,
        user_id=user_id,
    )

    try:
        user: User | None = await user_dao.get_user()
        if user is None:
            user: User = await user_dao.add_user()

        await dialog_manager.start(
            state=StartSG.main,
            mode=StartMode.RESET_STACK,
        )

    except SQLAlchemyError:
        logger.error(
            "Ошибка при попытке получить/обновить данные %s",
            User.__name__,
            exc_info=True,
        )
        await message.answer(
            "🆘 Произошла ошибка, попробуйте еще раз"
        )


@start_router.message(F.text == "/update")
async def update_window(
    message: Message,
    dialog_manager: DialogManager
) -> None:

    if dialog_manager.has_context():
        await dialog_manager.update(dialog_manager.dialog_data)


start_dialog = Dialog(
    Window(
        Jinja(
            text="<b>💬 Привет, добавь почту или "
                 "выбери существующую</b>",
        ),
        Row(
            Button(
                text=Const("🆕 Добавить почту"),
                id="btn_add_mail",
                on_click=to_add_mail,
            ),
            Button(
                text=Const("📫 Моя почта"),
                id="btn_my_mail",
                on_click=to_select_mail,
            ),
        ),
        state=StartSG.main,
    ),
)
