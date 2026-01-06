from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities.context import Context


async def get_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, list[tuple[str, str]]]:

    #  radio_items = [("mail.ru", "1"), ("yandex.ru", "2")]
    radio_items: list[tuple[str, str]] = \
        dialog_manager.start_data.get("radio_mail_host")

    context: Context = dialog_manager.current_context()

    name_mail: str | None = context.widget_data.get("login")
    password_mail: str | None = context.widget_data.get("password")

    return {
        "radio": radio_items,
        "name_mail": name_mail,
        "password_mail": password_mail
    }
