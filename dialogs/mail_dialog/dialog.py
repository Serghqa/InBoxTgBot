from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Radio, Column, Row
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from operator import itemgetter

from dialogs.states import Mail


mail_dialog = Dialog(
    Window(
        Format(
            text="Почта"
        ),
        state=Mail.main,
    ),
)
