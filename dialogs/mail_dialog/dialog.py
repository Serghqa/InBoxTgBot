from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Radio, Column, Row
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from operator import itemgetter

from .getters import get_data
from .handlers import exit_mail
from dialogs.states import Mail


mail_dialog = Dialog(
    Window(
        Format(
            text="Почта {login}"
        ),
        Button(
            text=Const("Выйти"),
            id="btn_exit",
            on_click=exit_mail,
        ),
        getter=get_data,
        state=Mail.main,
    ),
)
