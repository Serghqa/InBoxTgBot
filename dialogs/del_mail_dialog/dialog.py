from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from .handlers import to_select_mail, del_mail
from .getters import get_data
from dialogs.states import DelMail


del_mail_dialog = Dialog(
    Window(
        Format(
            text="Удалить почту {login}",
        ),
        Row(
            Button(
                text=Const("Удалить"),
                id="btn_del",
                on_click=del_mail,
            ),
            Button(
                text=Const("Назад"),
                id="btn_back",
                on_click=to_select_mail,
            ),
        ),
        getter=get_data,
        state=DelMail.main,
    ),
)
