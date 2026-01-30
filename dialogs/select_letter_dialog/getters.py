from aiogram_dialog import DialogManager


async def get_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:

    messages: dict = dialog_manager.start_data.get("messages")

    select_ids = [(data["sender"], ids) for ids, data in messages.items()]
    str_period: str = dialog_manager.start_data.get("period")
    return {
        "select_ids": select_ids,
        "period": str_period,
    }
