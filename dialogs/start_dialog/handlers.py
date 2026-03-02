import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.exc import SQLAlchemyError

from db.models import ImapCredentials
from db.services import UserDAO
from dialogs.states import AddMail, SelectMail
from schemas import ImapSettings


logger = logging.getLogger(__name__)


async def to_add_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.start(
        state=AddMail.main,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
    )


async def to_select_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    user_dao = UserDAO(dialog_manager)
    try:
        user_credentials: list[ImapCredentials] = \
            await user_dao.get_user_credentials()
    except SQLAlchemyError:
        logger.error(
            "Ошибка загрузки данных пользователя user_id=%s",
            user_dao.user_id,
            exc_info=True,
        )
        await callback.answer(
            text="🆘 Произошла ошибка, попробуйте еще раз",
            show_alert=True,
        )
        return
    radio_imap_credentials = []
    data_imap_credentials = {}
    for item, credentials in enumerate(user_credentials, 1):
        radio_imap_credentials.append((credentials.email, str(item)))

        imap_settings = ImapSettings(**credentials.get_data())
        data_imap_credentials[str(item)] = imap_settings.model_dump()

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
