import logging

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import (
    DialogManager,
    ShowMode,
    StartMode,
)
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from db.services import SecureEncryptor
from dialogs.states import Mail


logger = logging.getLogger(__name__)


async def cancel_password(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.done(
        show_mode=ShowMode.EDIT,
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
        await message.delete()

        login: str = dialog_manager.start_data.get("login")
        host: str = dialog_manager.start_data.get("host")
        encrypted_password: str = encryptor.encrypt_data(message.text)
        start_data = {
            "login": login,
            "host": host,
            "password": encrypted_password,
        }
        dialog_manager.dialog_data["password_incorrect"] = False

        await dialog_manager.start(
            state=Mail.main,
            data=start_data,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.SEND,
        )
    else:
        dialog_manager.dialog_data["password_incorrect"] = True
