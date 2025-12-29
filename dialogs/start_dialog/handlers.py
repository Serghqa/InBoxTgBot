import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button

from states import AddMail


logger = logging.getLogger(__name__)


async def to_add_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    start_data = {
        "radio_mail_host": [
            ("mail.ru", "1"),
            ("yandex.ru", "2")
        ]
    }

    await dialog_manager.start(
        state=AddMail.main,
        data=start_data,
        show_mode=ShowMode.EDIT,
    )
