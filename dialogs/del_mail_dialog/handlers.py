import logging

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.exc import SQLAlchemyError

from db.models import ImapCredentials
from db.services import UserDAO, SecureEncryptor
from dialogs.states import SelectMail, DelMail


logger = logging.getLogger(__name__)


async def _set_start_data(user_dao: UserDAO) -> dict:

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

    user_dao = UserDAO(dialog_manager)

    try:
        start_data = await _set_start_data(user_dao)

        await dialog_manager.start(
            state=SelectMail.main,
            data=start_data,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.EDIT,
        )
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


async def del_mail(
    message: Message,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    user_dao = UserDAO(dialog_manager)
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

        await user_dao.session.commit()

        await dialog_manager.switch_to(
            state=DelMail.deleted,
            show_mode=ShowMode.EDIT,
        )

    except SQLAlchemyError:
        logger.error(
            "Ошибка при попытке удалить %s user_id=%s",
            ImapCredentials.__name__, user_dao.user_id,
            exc_info=True,
        )
        await message.answer(
            text="🆘 Произошла неожиданная ошибка, попробуйте еще раз"
        )


async def password_validate(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager
) -> None:

    user_id: int = dialog_manager.event.from_user.id
    encryptor = SecureEncryptor(user_id)

    pwd_hash_str: str = dialog_manager.start_data.get("password")
    result_password = encryptor.authenticate(message.text, pwd_hash_str)

    if result_password:
        dialog_manager.dialog_data["is_password"] = False
        await message.delete()

        await dialog_manager.switch_to(
            state=DelMail.deletion,
            show_mode=ShowMode.EDIT,
        )
    else:
        dialog_manager.dialog_data["is_password"] = True


async def cancel_delete(
    message: Message,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.switch_to(
        state=DelMail.main,
        show_mode=ShowMode.EDIT,
    )
