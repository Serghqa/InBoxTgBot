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
from aiogram_dialog.widgets.text import Const, Format

from .handlers import (
    to_add_mail,
)
from states import StartSG


start_router = Router()


@start_router.message(F.text, CommandStart())
async def command_start(
    message: Message,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.start(
        state=StartSG.main,
        mode=StartMode.RESET_STACK,
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
        Format(
            text="Привет, добавь почту или "
                 "выбери существующую.",
        ),
        Row(
            Button(
                text=Const("Добавить почту"),
                id="btn_add_mail",
                on_click=to_add_mail,
            ),
            Button(
                text=Const("Моя почта"),
                id="btn_my_mail",
            ),
        ),
        state=StartSG.main,
    ),
)
