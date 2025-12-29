import logging

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import (
    Data,
    DialogManager,
    ShowMode,
)
from aiogram_dialog.api.entities.context import Context
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput

from states import AddMail


logger = logging.getLogger(__name__)


async def back_to_start_dlg(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.done(
        show_mode=ShowMode.EDIT,
    )


async def process_start(
    start_data: Data,
    dialog_manager: DialogManager
) -> None:

    context: Context = dialog_manager.current_context()
    context.widget_data["radio_mail_host"] = "1"


def input_validate(text: str) -> str:

    return text


async def success_login(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str
) -> None:

    dialog_manager.dialog_data["name_mail"] = text
    await message.delete()
    await dialog_manager.switch_to(
        state=AddMail.password,
        show_mode=ShowMode.EDIT,
    )


async def success_password(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str
) -> None:

    dialog_manager.dialog_data["password_mail"] = text
    await message.delete()
    await dialog_manager.switch_to(
        state=AddMail.add_mail,
        show_mode=ShowMode.EDIT,
    )


async def input_error(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError
) -> None:

    pass


async def cancel_add_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    dialog_manager.dialog_data.clear()
    await dialog_manager.switch_to(
        state=AddMail.main,
        show_mode=ShowMode.EDIT,
    )


async def add_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.switch_to(
        state=AddMail.success_mail,
        show_mode=ShowMode.EDIT,
    )
