from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Group, Row
from aiogram_dialog.widgets.text import Const, Format

from dialogs.states import ReadingMail


reading_mail_dialog = Dialog(
    Window(
        Format(
            text="Чтение почты",
        ),
        state=ReadingMail.main,
    ),
)
