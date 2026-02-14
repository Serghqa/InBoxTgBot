from aiogram_dialog import DialogManager


async def get_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, str]:

    data = {}

    mail_is_none: bool = dialog_manager.dialog_data.get("mail_is_none", False)
    data["mail_is_none"] = mail_is_none
    data.update(dialog_manager.start_data)

    return data
