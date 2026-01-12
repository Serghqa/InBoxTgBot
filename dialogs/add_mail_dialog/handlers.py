import logging

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import (
    Data,
    DialogManager,
    ShowMode,
    StartMode,
)
from aiogram_dialog.api.entities.context import Context
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput
from email_validator import validate_email, EmailNotValidError
from imapclient import IMAPClient
from imapclient.exceptions import IMAPClientError, LoginError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ImapCredentials
from db.services import UserDAO, SecureEncryptor
from dialogs.states import AddMail, Mail, StartSG


logger = logging.getLogger(__name__)


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


async def process_start(
    start_data: Data,
    dialog_manager: DialogManager
) -> None:

    context: Context = dialog_manager.current_context()
    context.widget_data["radio_mail_host"] = "1"


def login_validate(text: str) -> str:

    try:
        validate_email(text, check_deliverability=False)
    except EmailNotValidError:
        raise ValueError

    return text


def password_validate(text: str) -> str:

    return text


async def success_login(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str
) -> None:

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

    user_id: int = dialog_manager.event.from_user.id
    context: Context = dialog_manager.current_context()
    host_item: str = context.widget_data.get("radio_mail_host")
    hosts: dict[str, str] = dialog_manager.start_data.get("hosts")
    host: str = hosts.get(host_item)

    name_mail: str = context.widget_data.get("login")
    password_mail: str = text

    try:
        with IMAPClient(host) as client:
            client.login(name_mail, password_mail)
    except LoginError:
        await message.answer("Неверный логин или пароль, попробуйте еще раз.")
        return
    except IMAPClientError:
        logger.error("Ошибка подключения imapclient", exc_info=True)
        await message.answer(
            "Произошла ошибка подключения к почте, попробуйте еще раз"
        )
        return

    dialog_manager.dialog_data["host"] = host

    encrypted = SecureEncryptor(user_id)
    encrypted_password: str = encrypted.encrypt_data(password_mail)
    widget.set_widget_data(dialog_manager, encrypted_password)

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

    await message.answer("Недопустимый формат")


async def cancel_add_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    context: Context = dialog_manager.current_context()
    context.widget_data.pop("login", None)
    context.widget_data.pop("password", None)

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

    context: Context = dialog_manager.current_context()

    session: AsyncSession = dialog_manager.middleware_data.get("db_session")
    name_mail: str = context.widget_data.get("login")
    encrypted_password: str = context.widget_data.get("password")
    host: str = dialog_manager.dialog_data.get("host")
    user_id: int = dialog_manager.event.from_user.id

    user_dao = UserDAO(session, user_id)
    encryptor = SecureEncryptor(user_id)

    password: str = encryptor.decrypted_data(encrypted_password)
    pwd_hash_str: str = encryptor.generate_hash_str(password)

    try:
        imap_credentials: ImapCredentials | None = \
            await user_dao.get_imap_credentials(
                email=name_mail,
                imap_server=host,
            )
        if imap_credentials is not None:
            await callback.answer(
                text="Эта почта уже добавлена.",
                show_alert=True,
            )
            return

        await user_dao.add_imap_credentials(
            email=name_mail,
            password=pwd_hash_str,
            imap_server=host,
        )
    except SQLAlchemyError:
        logger.error(
            "Ошибка при попытке получить/добавить %s",
            ImapCredentials.__name__,
            exc_info=True,
        )
        await callback.answer(
            text="Произошла ошибка, попробуйте еще раз.",
            show_alert=True,
        )
        return

    await dialog_manager.switch_to(
        state=AddMail.success_mail,
        show_mode=ShowMode.EDIT,
    )


async def to_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    context: Context = dialog_manager.current_context()

    host: str = dialog_manager.dialog_data.get("host")
    name_mail: str = context.widget_data.get("login")
    encrypted_password: str = context.widget_data.get("password")

    start_data = {
        "host": host,
        "login": name_mail,
        "password": encrypted_password,
    }

    await dialog_manager.start(
        state=Mail.main,
        data=start_data,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
    )
