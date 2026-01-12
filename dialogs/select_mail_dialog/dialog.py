from aiogram import F
from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Radio, Column, Row
from aiogram_dialog.widgets.text import Const, Format
from operator import itemgetter

from .getters import get_data
from .handlers import process_start, to_mail, back_to_start_dlg, to_del_mail
from dialogs.states import SelectMail


select_mail_dialog = Dialog(
    Window(
        Format(
            text="Выберите почту",
        ),
        Column(
            Radio(
                Format(
                    text='☑️ {item[0]}',
                ),
                Format(
                    text='⬜ {item[0]}',
                ),
                id="radio_mail_select",
                item_id_getter=itemgetter(1),
                items="radio",
            ),
        ),
        Row(
            Button(
                Const("К почте"),
                id="btn_to_mail",
                on_click=to_mail,
            ),
            Button(
                Const("Удалить почту"),
                id="btn_to_del",
                on_click=to_del_mail,
            ),
            when=F["is_mail"],
        ),
        Button(
            Const("Назад"),
            id="btn_back",
            on_click=back_to_start_dlg,
        ),
        getter=get_data,
        state=SelectMail.main,
    ),
    on_start=process_start,
)
