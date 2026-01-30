from aiogram_dialog import DialogManager


def truncate_sender(sender: str, max_length: int = 25) -> str:

    if len(sender) <= max_length:
        return sender

    return f"{sender[:max_length-10]}...{sender[-7:]}"


async def get_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:

    messages: dict = dialog_manager.start_data.get("messages")

    select_ids = [
        (truncate_sender(data["sender"]), ids)
        for ids, data in messages.items()
    ]
    str_period: str = dialog_manager.start_data.get("period")
    return {
        "select_ids": select_ids,
        "period": str_period,
    }
