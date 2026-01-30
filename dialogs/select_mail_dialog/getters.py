from aiogram_dialog import DialogManager


def truncate_address(address: str, max_length: int = 25) -> str:

    if len(address) <= max_length:
        return address

    return f"{address[:max_length-10]}...{address[-9:]}"


async def get_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, list[tuple[str, str]]]:

    #  radio_items = [("mail.ru", "1"), ("yandex.ru", "2"), ...]
    radio_items: list[tuple[str, str]] = [
        (truncate_address(address), item)
        for address, item in dialog_manager.start_data.get("radio_mail_select")
    ]
    is_mail: bool = len(radio_items) > 0

    return {
        "radio": radio_items,
        "is_mail": is_mail,
    }
