import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import (
    Data,
    DialogManager,
    ShowMode,
    StartMode,
)
from aiogram_dialog.api.entities.context import Context
from aiogram_dialog.widgets.kbd import Button

from states import Mail, StartSG, DelMail


logger = logging.getLogger(__name__)


def _get_imap_data(dialog_manager: DialogManager) -> dict[str, str]:

    data = {}

    context: Context = dialog_manager.current_context()
    widget_item: str = context.widget_data.get("radio_mail_select")
    if widget_item:
        imap_credentials: dict[str, dict] = \
            dialog_manager.start_data.get("imap_credentials")
        if imap_credentials:
            imap_data: dict = imap_credentials.get(widget_item)
            if imap_data:
                host: str = imap_data.get("imap_server")
                name_mail: str = imap_data.get("email")
                encrypted_password: str = imap_data.get("password")

                data = {
                    "host": host,
                    "login": name_mail,
                    "password": encrypted_password,
                }

    return data


async def process_start(
    start_data: Data,
    dialog_manager: DialogManager
) -> None:

    radio_imap_credentials: list[tuple[str, str]] = \
        dialog_manager.start_data.get("radio_mail_select")

    if radio_imap_credentials:
        context: Context = dialog_manager.current_context()
        context.widget_data["radio_mail_select"] = "1"


async def to_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    start_data = _get_imap_data(dialog_manager)
    if start_data:
        await dialog_manager.start(
            state=Mail.main,
            data=start_data,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.EDIT,
        )


async def to_del_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    start_data: dict[str, str] = _get_imap_data(dialog_manager)
    if start_data:
        await dialog_manager.start(
            state=DelMail.main,
            data=start_data,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.EDIT,
        )


async def back_to_start_dlg(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.start(
        state=StartSG.main,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
    )
