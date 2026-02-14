from aiogram import F
from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format, Jinja
from operator import itemgetter

from .getters import get_data
from .handlers import (
    exit_mail,
    to_find_mail,
    to_main,
    shift_year,
    process_clicked,
    CustomSelect,
    process_result,
)
from dialogs.states import Mail


mail_dialog = Dialog(
    Window(
        Jinja(
            text="<b>Почта {{login}}</b>",
        ),
        Jinja(
            text="<i>Ищу почту...</i>",
            when=F["find_mail"],
        ),
        Row(
            Button(
                text=Const("🔎 Найти почту"),
                id="btn_find_mail",
                on_click=to_find_mail,
            ),
            Button(
                text=Const("🚪Выйти"),
                id="btn_exit",
                on_click=exit_mail,
            ),
        ),
        state=Mail.main,
    ),
    Window(
        Jinja(
            text="<b>🗓️ Выбери месяц</b>",
        ),
        Jinja(
            text="<i>Ищу почту...</i>",
            when=F["find_mail"],
        ),
        Jinja(
            text="<i>Загружаю письма...</i>",
            when=F["load_mail"],
        ),
        Button(
            text=Format(
                text="{year}"
            ),
            id="btn_year",
        ),
        CustomSelect(
            text=Format("{item[0]} {item[2]}"),
            id="custom_select",
            item_id_getter=itemgetter(1),
            items="data_select",
            on_click=process_clicked,
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
        Button(
            text=Const("⬅️ Назад"),
            id="btn_back_main",
            on_click=to_main,
        ),
        on_process_result=process_result,
        state=Mail.calendar,
    ),
    getter=get_data,
)
