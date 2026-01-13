from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from .getters import get_data
from .handlers import (
    exit_mail,
    to_find_receipts,
    on_date_select,
    CustomCalendar,
)
from dialogs.states import Mail


mail_dialog = Dialog(
    Window(
        Format(
            text="Почта {login}",
        ),
        Row(
            Button(
                text=Const("Найти квитанции"),
                id="btn_find_receipts",
                on_click=to_find_receipts,
            ),
            Button(
                text=Const("Выйти"),
                id="btn_exit",
                on_click=exit_mail,
            ),
        ),
        getter=get_data,
        state=Mail.main,
    ),
    Window(
        Format(
            text="Выбери дату",
        ),
        CustomCalendar(
            id="calendar",
            on_click=on_date_select,
        ),
        state=Mail.calendar,
    ),
)
