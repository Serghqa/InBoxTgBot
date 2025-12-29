from aiogram_dialog import DialogManager


async def get_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, list[tuple[str, str]]]:

    #  radio_items = [("mail.ru", "1"), ("yandex.ru", "2")]
    radio_items: list[tuple[str, str]] = \
        dialog_manager.start_data.get("radio_mail_host")

    name_mail: str | None = dialog_manager.dialog_data.get("name_mail")
    password_mail: str | None = dialog_manager.dialog_data.get("password_mail")

    return {
        "radio": radio_items,
        "name_mail": name_mail,
        "password_mail": password_mail
    }
