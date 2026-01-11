from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities.context import Context

from db.services import SecureEncryptor


async def get_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, list[tuple[str, str]]]:

    #  radio_items = [("mail.ru", "1"), ("yandex.ru", "2")]
    radio_items: list[tuple[str, str]] = \
        dialog_manager.start_data.get("radio_mail_host")

    return {
        "radio": radio_items,
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

    return {
        "name_mail": name_mail,
        "password_mail": password_mail
    }
