import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from config import load_config, Config
from states import AddMail


MAIL_ITEM = "1"
YANDEX_ITEM = "2"

logger = logging.getLogger(__name__)


async def to_add_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    config: Config = load_config()

    start_data = {
        "radio_mail_host": [
            ("mail.ru", MAIL_ITEM),
            ("yandex.ru", YANDEX_ITEM),
        ],
        "hosts": {
            MAIL_ITEM: config.inbox.MAIL_SERVER,
            YANDEX_ITEM: config.inbox.YANDEX_SERVER,
        },
    }

    await dialog_manager.start(
        state=AddMail.main,
        data=start_data,
        show_mode=ShowMode.EDIT,
    )
