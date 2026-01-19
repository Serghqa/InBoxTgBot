from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Group, Row
from aiogram_dialog.widgets.text import Const, Format

from .getters import get_data
from .handlers import (
    exit_mail,
    to_find_receipts,
    to_main,
    shift_year,
    process_clicked,
    buttons,
)
from dialogs.states import Mail


button_months = [
    Button(
        text=Const(month_name),
        id=button_id,
        on_click=process_clicked,
    ) for button_id, month_name in buttons.items()
]


mail_dialog = Dialog(
    Window(
        Format(
            text="Почта {login}",
        ),
        Row(
            Button(
                text=Const("Найти почту"),
                id="btn_find_receipts",
                on_click=to_find_receipts,
            ),
            Button(
                text=Const("Выйти"),
                id="btn_exit",
                on_click=exit_mail,
            ),
        ),
        state=Mail.main,
    ),
    Window(
        Format(
            text="Выбери месяц",
        ),
        Button(
            text=Format(
                text="{year}"
            ),
            id="btn_year",
        ),
        Group(
            Row(
                *button_months[:4],
            ),
            Row(
                *button_months[4:8],
            ),
            Row(
                *button_months[8:]
            ),
            Row(
                Button(
                    text=Const("◀️"),
                    id="btn_prev",
                    on_click=shift_year,
                ),
                Button(
                    text=Const("▶️"),
                    id="btn_next",
                    on_click=shift_year,
                ),
            ),
        ),
        Button(
            text=Const("Назад"),
            id="btn_back_main",
            on_click=to_main,
        ),
        state=Mail.calendar,
    ),
    getter=get_data,
)
