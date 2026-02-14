from aiogram_dialog import DialogManager
from datetime import datetime
from zoneinfo import ZoneInfo


async def get_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict[str, str]:

    tz = ZoneInfo("Asia/Yekaterinburg")
    today = datetime.now(tz)

    year: int = dialog_manager.dialog_data.setdefault("year", today.year)
    months_abbr: list[str] = dialog_manager.dialog_data.get("months_abbr", [])
    messages: list[int] = dialog_manager.dialog_data.get("messages", [])
    data_select: list[str, int, int] = [
        (abbr, item, count)
        for item, (abbr, count) in enumerate(zip(months_abbr, messages), 1)
    ]

    find_mail: bool = dialog_manager.dialog_data.get("find_mail", False)
    load_mail: bool = dialog_manager.dialog_data.get("load_mail", False)

    data = {
        "year": year,
        "months_abbr": months_abbr,
        "messages": messages,
        "data_select": data_select,
        "find_mail": find_mail,
        "load_mail": load_mail,
    }
    data.update(dialog_manager.start_data)

    return data
