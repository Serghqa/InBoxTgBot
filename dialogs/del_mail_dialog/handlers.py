import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from db.models import ImapCredentials
from db.services import UserDAO
from dialogs.states import SelectMail


logger = logging.getLogger(__name__)


async def _set_start_data(
    session: AsyncSession,
    user_id: int
) -> dict:

    user_dao = UserDAO(session, user_id)

    user_credentials: list[ImapCredentials] = \
        await user_dao.get_user_credentials()
    radio_imap_credentials = []
    data_imap_credentials = {}
    for item, credentials in enumerate(user_credentials, 1):
        radio_imap_credentials.append((credentials.email, str(item)))
        data_imap_credentials[str(item)] = credentials.get_data()

    return {
        "radio_mail_select": radio_imap_credentials,
        "imap_credentials": data_imap_credentials,
    }


async def to_select_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    session: AsyncSession = dialog_manager.middleware_data.get("db_session")
    user_id: int = dialog_manager.event.from_user.id

    try:
        start_data = await _set_start_data(
            session=session,
            user_id=user_id,
        )

        await dialog_manager.start(
            state=SelectMail.main,
            data=start_data,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.EDIT,
        )
    except SQLAlchemyError:
        logger.error(
            "Ошибка загрузки данных пользователя user_id=%s",
            user_id,
            exc_info=True,
        )
        await callback.answer(
            text="🆘 Произошла ошибка, попробуйте еще раз",
            show_alert=True,
        )


async def del_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    session: AsyncSession = dialog_manager.middleware_data.get("db_session")
    user_id: int = dialog_manager.event.from_user.id

    user_dao = UserDAO(session, user_id)
    email: str = dialog_manager.start_data.get("login")
    host: str = dialog_manager.start_data.get("host")

    try:
        result: ImapCredentials | None = await user_dao.del_imap_credentials(
            email=email,
            imap_server=host,
        )

        if result is None:
            dialog_manager.dialog_data["mail_is_none"] = True
            return

        dialog_manager.dialog_data["mail_is_none"] = False

        start_data: dict = await _set_start_data(
            session=session,
            user_id=user_id,
        )
        await session.commit()

        await dialog_manager.start(
            state=SelectMail.main,
            data=start_data,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.EDIT,
        )
    except SQLAlchemyError:
        logger.error(
            "Ошибка при попытке удалить %s user_id=%s",
            ImapCredentials.__name__, user_id,
            exc_info=True,
        )
        await callback.answer(
            text="🆘 Произошла неожиданная ошибка, попробуйте еще раз",
            show_alert=True,
        )
