import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import (
    DialogManager,
    ShowMode,
    StartMode,
)
from aiogram_dialog.widgets.kbd import (
    Button,
)
from datetime import datetime
from zoneinfo import ZoneInfo

from dialogs.states import StartSG, Mail


logger = logging.getLogger(__name__)


buttons = {
    "btn_january": "Январь",
    "btn_february": "Февраль",
    "btn_march": "Март",
    "btn_april": "Апрель",
    "btn_may": "Май",
    "btn_june": "Июнь",
    "btn_jule": "Июль",
    "btn_august": "Август",
    "btn_september": "Сентябрь",
    "btn_october": "Октябрь",
    "btn_november": "Ноябрь",
    "btn_december": "Декабрь",
}


async def exit_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.start(
        state=StartSG.main,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
    )


async def to_find_receipts(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.switch_to(
        state=Mail.calendar,
        show_mode=ShowMode.EDIT,
    )


async def to_main(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.switch_to(
        state=Mail.main,
        show_mode=ShowMode.EDIT,
    )


async def shift_year(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    tz = ZoneInfo("Asia/Yekaterinburg")
    today = datetime.now(tz)

    year: int = dialog_manager.dialog_data.get("year", today.year)
    if widget.widget_id == "btn_prev":
        year -= 1
    if widget.widget_id == "btn_next":
        year += 1

    dialog_manager.dialog_data["year"] = year


async def process_clicked(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    pass
