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

    data = {
        "year": year,
    }
    data.update(dialog_manager.start_data)

    return data
