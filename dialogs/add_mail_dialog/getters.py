from aiogram_dialog import DialogManager

from config import load_config, Config
from db.services import SecureEncryptor


def _truncate_data(data: str, max_length: int = 25) -> str:

    if len(data) <= max_length:
        return data

    return f"{data[:max_length-10]}...{data[-7:]}"


async def get_data_servers(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, list[tuple[str, str]]]:

    config: Config = load_config()
    #  radio_items = [("mail.ru", "1"), ("yandex.ru", "2")]
    radio_items = [
        (server, str(item))
        for item, server in enumerate(config.inbox.get_ordered_servers(), 1)
    ]
    return {
        "radio": radio_items,
    }


async def get_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, str]:

    login_err: bool = dialog_manager.dialog_data.get("login_err", False)
    passwor_err: bool = dialog_manager.dialog_data.get("password_err", False)
    auth_err: bool = dialog_manager.dialog_data.get("auth_err", False)

    return {
        "login_err": login_err,
        "password_err": passwor_err,
        "auth_err": auth_err,
    }


async def get_login(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, str]:

    email: str = dialog_manager.dialog_data.get("email")

    return {
        "email": _truncate_data(email),
    }


async def get_data_mail(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, str | bool]:

    user_id: int = dialog_manager.event.from_user.id
    encryptor = SecureEncryptor(user_id)

    name_mail: str = dialog_manager.dialog_data.get("email")
    encrypted_password: str = dialog_manager.dialog_data.get("password")
    password_mail = encryptor.decrypted_data(encrypted_password)

    is_mail: bool = dialog_manager.dialog_data.get("is_mail", False)

    return {
        "name_mail": _truncate_data(name_mail),
        "password_mail": _truncate_data(password_mail),
        "is_mail": is_mail,
    }
