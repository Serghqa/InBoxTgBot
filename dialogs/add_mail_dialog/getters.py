from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities.context import Context

from db.services import SecureEncryptor


def _truncate_data(data: str, max_length: int = 25) -> str:

    if len(data) <= max_length:
        return data

    return f"{data[:max_length-10]}...{data[-7:]}"


async def get_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, list[tuple[str, str]]]:

    #  radio_items = [("mail.ru", "1"), ("yandex.ru", "2")]
    hosts: dict[str, str] = dialog_manager.start_data.get("hosts")
    radio_items: list[tuple[str, str]] = [
        (host, item) for item, host in hosts.items()
    ]
    login_err: bool = dialog_manager.dialog_data.get("login_err", False)
    passwor_err: bool = dialog_manager.dialog_data.get("password_err", False)
    auth_err: bool = dialog_manager.dialog_data.get("auth_err", False)

    return {
        "radio": radio_items,
        "login_err": login_err,
        "password_err": passwor_err,
        "auth_err": auth_err,
    }


async def get_login(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, str]:

    context: Context = dialog_manager.current_context()
    login: str = context.widget_data.get("login")

    return {
        "login": _truncate_data(login),
    }


async def get_data_mail(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, str]:

    context: Context = dialog_manager.current_context()
    user_id: int = dialog_manager.event.from_user.id
    encryptor = SecureEncryptor(user_id)

    name_mail: str = context.widget_data.get("login")
    encrypted_password: str = context.widget_data.get("password")
    password_mail = encryptor.decrypted_data(encrypted_password)

    is_mail: bool = dialog_manager.dialog_data.get("is_mail", False)

    return {
        "name_mail": _truncate_data(name_mail),
        "password_mail": _truncate_data(password_mail),
        "is_mail": is_mail,
    }
