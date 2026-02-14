from aiogram_dialog import DialogManager


async def get_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, str]:

    data = {}
    password_incorrect: bool = \
        dialog_manager.dialog_data.get("password_incorrect", False)
    data["password_incorrect"] = password_incorrect
    data.update(dialog_manager.start_data)

    return data
