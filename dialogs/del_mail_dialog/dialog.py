from aiogram import F
from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Jinja

from .handlers import to_select_mail, del_mail
from .getters import get_data
from dialogs.states import DelMail


del_mail_dialog = Dialog(
    Window(
        Jinja(
            text="<b>❓ Удалить почту {{login}}</b>",
        ),
        Jinja(
            text="<code>🚫 Такой почты не существует</code>",
            when=F["mail_is_none"],
        ),
        Row(
            Button(
                text=Const("⬅️ Назад"),
                id="btn_back",
                on_click=to_select_mail,
            ),
            Button(
                text=Const("🗑️ Удалить"),
                id="btn_del",
                on_click=del_mail,
            ),
        ),
        getter=get_data,
        state=DelMail.main,
    ),
)
