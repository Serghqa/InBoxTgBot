from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Jinja
from aiogram_dialog.widgets.input import MessageInput

from .handlers import (
    cancel_password,
    password_validate,
)
from .getters import get_data
from dialogs.states import PasswordMail


password_mail_dialog = Dialog(
    Window(
        Jinja(
            text="<b>Отправь пароль от почты {{login}}</b>",
        ),
        Jinja(
            text="<code>🚫 Неверный пароль</code>",
            when=F["password_incorrect"],
        ),
        MessageInput(
            func=password_validate,
            content_types=ContentType.TEXT,
        ),
        Button(
            text=Const("❌ Отмена"),
            id="btn_cancel",
            on_click=cancel_password,
        ),
        getter=get_data,
        state=PasswordMail.main,
    ),
)
