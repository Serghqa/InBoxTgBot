from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Radio, Column, Row
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from operator import itemgetter

from .getters import get_data
from states import SelectMail


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
        getter=get_data,
        state=SelectMail.main,
    ),
)
