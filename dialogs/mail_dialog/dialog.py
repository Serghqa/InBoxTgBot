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
        state=Mail.main,
    ),
    Window(
        Format(
            text="Выбери дату",
        ),
        Button(
            text=Format(
                text="{year}"
            ),
            id="btn_year",
        ),
        Group(
            Row(
                Button(
                    text=Const("Январь"),
                    id="btn_january",
                ),
                Button(
                    text=Const("Февраль"),
                    id="btn_february",
                ),
                Button(
                    text=Const("Март"),
                    id="btn_march",
                ),
                Button(
                    text=Const("Апрель"),
                    id="btn_april",
                ),
            ),
            Row(
                Button(
                    text=Const("Май"),
                    id="btn_may",
                ),
                Button(
                    text=Const("Июнь"),
                    id="btn_june",
                ),
                Button(
                    text=Const("Июль"),
                    id="btn_jule",
                ),
                Button(
                    text=Const("Август"),
                    id="btn_august",
                ),
            ),
            Row(
                Button(
                    text=Const("Сентябрь"),
                    id="btn_september",
                ),
                Button(
                    text=Const("Октябрь"),
                    id="btn_october",
                ),
                Button(
                    text=Const("Ноябрь"),
                    id="btn_november",
                ),
                Button(
                    text=Const("Декабрь"),
                    id="btn_december",
                ),
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
