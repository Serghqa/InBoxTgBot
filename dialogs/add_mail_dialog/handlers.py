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
from typing import Any

from config import load_config, Config
from db.models import ImapCredentials
from db.services import UserDAO, SecureEncryptor
from dialogs.states import AddMail, Mail, StartSG
from schemas import ImapSettings


logger = logging.getLogger(__name__)


def _set_widget_data(
    context: Context,
    widget_id: str,
    value: Any
) -> dict:

    context.widget_data[widget_id] = value

    return context.widget_data


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
    _set_widget_data(
        context=context,
        widget_id="radio_mail_host",
        value="1",
    )


def login_validate(text: str) -> str:

    try:
        validate_email(text, check_deliverability=False)
    except EmailNotValidError:
        raise ValueError

    return text


def password_validate(text: str) -> str:

    if not text.isascii():
        raise ValueError

    return text


async def success_login(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    text: str
) -> None:

    dialog_manager.dialog_data["login_err"] = False
    dialog_manager.dialog_data["email"] = text

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

    config: Config = load_config()
    user_id: int = dialog_manager.event.from_user.id
    context: Context = dialog_manager.current_context()
    host_item: str = context.widget_data.get("radio_mail_host")

    hosts = {
        str(item): server
        for item, server in enumerate(config.inbox.get_ordered_servers(), 1)
    }

    host: str = hosts.get(host_item)

    name_mail: str = dialog_manager.dialog_data.get("email")
    password_mail: str = text

    dialog_manager.dialog_data["password_err"] = False
    dialog_manager.dialog_data["auth_err"] = False

    try:
        with IMAPClient(host) as client:
            client.login(name_mail, password_mail)
            await message.delete()

            encrypted = SecureEncryptor(user_id)
            encrypted_password: str = encrypted.encrypt_data(password_mail)
            context.widget_data["password"] = encrypted_password
            dialog_manager.dialog_data["imap_server"] = host
            dialog_manager.dialog_data["password"] = encrypted_password

            await dialog_manager.switch_to(
                state=AddMail.add_mail,
                show_mode=ShowMode.EDIT,
            )
    except LoginError:
        dialog_manager.dialog_data["auth_err"] = True

    except IMAPClientError:
        logger.error("Ошибка подключения imapclient", exc_info=True)
        await message.answer(
            text="🆘 Ошибка подключения",
        )


async def login_error(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError
) -> None:

    dialog_manager.dialog_data["login_err"] = True


async def password_error(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError
) -> None:

    dialog_manager.dialog_data["password_err"] = True
    dialog_manager.dialog_data["auth_err"] = False


async def cancel_add_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    context: Context = dialog_manager.current_context()
    widget_id_radio: str = context.widget_data.get("radio_mail_host")
    context.widget_data.clear()
    dialog_manager.dialog_data.clear()

    _set_widget_data(
        context=context,
        widget_id="radio_mail_host",
        value=widget_id_radio,
    )

    await dialog_manager.switch_to(
        state=AddMail.main,
        show_mode=ShowMode.EDIT,
    )


async def add_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    imap_settings = ImapSettings(**dialog_manager.dialog_data)
    encrypted_password: str = imap_settings.password

    user_dao = UserDAO(dialog_manager)
    encryptor = SecureEncryptor(user_dao.user_id)

    password: str = encryptor.decrypted_data(encrypted_password)
    pwd_hash_str: str = encryptor.generate_hash_str(password)

    try:
        imap_credentials: ImapCredentials | None = \
            await user_dao.get_imap_credentials(
                email=imap_settings.email,
                imap_server=imap_settings.imap_server,
            )
        if imap_credentials is not None:
            dialog_manager.dialog_data["is_mail"] = True
            return

        dialog_manager.dialog_data["is_mail"] = False

        await user_dao.add_imap_credentials(
            email=imap_settings.email,
            password=pwd_hash_str,
            imap_server=imap_settings.imap_server,
        )
        await dialog_manager.switch_to(
            state=AddMail.success_mail,
            show_mode=ShowMode.EDIT,
        )
    except SQLAlchemyError:
        logger.error(
            "Ошибка при попытке получить/добавить %s",
            ImapCredentials.__name__,
            exc_info=True,
        )
        await callback.answer(
            text="🆘 Произошла ошибка, попробуйте еще раз",
            show_alert=True,
        )


async def to_login(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.switch_to(
        state=AddMail.login,
        show_mode=ShowMode.EDIT,
    )


async def to_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    imap_settings = ImapSettings(**dialog_manager.dialog_data)

    start_data = imap_settings.model_dump()

    await dialog_manager.start(
        state=Mail.main,
        data=start_data,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
    )
