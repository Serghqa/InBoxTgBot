import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from config import load_config, Config
from db.models import ImapCredentials
from db.services import UserDAO
from states import AddMail, SelectMail


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


async def to_select_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    session: AsyncSession = dialog_manager.middleware_data.get("db_session")
    user_id: int = dialog_manager.event.from_user.id

    user_dao = UserDAO(session, user_id)
    try:
        user_credentials: list[ImapCredentials] = \
            await user_dao.get_user_credentials()
    except SQLAlchemyError:
        logger.error(
            "Ошибка загрузки данных пользователя user_id=%s",
            user_id,
            exc_info=True,
        )
        await callback.answer(
            text="Произошла ошибка, попробуйте еще раз.",
            show_alert=True,
        )
        return
    radio_imap_credentials = []
    data_imap_credentials = {}
    for item, credentials in enumerate(user_credentials, 1):
        radio_imap_credentials.append((credentials.email, str(item)))
        key = f"{credentials.email}_{credentials.imap_server}"
        data_imap_credentials[key] = credentials.get_data()

    start_data = {
        "radio_mail_select": radio_imap_credentials,
        "imap_credentials": data_imap_credentials,
    }

    await dialog_manager.start(
        state=SelectMail.main,
        data=start_data,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
    )
