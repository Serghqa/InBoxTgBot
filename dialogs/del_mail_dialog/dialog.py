from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Jinja

from .handlers import (
    to_select_mail,
    del_mail,
    password_validate,
    cancel_delete,
)
from .getters import get_data
from dialogs.states import DelMail


del_mail_dialog = Dialog(
    Window(
        Jinja(
            text="<b>Для подтверждения удаления отправь "
            "пароль от почты {{email}}</b>",
        ),
        Jinja(
            text="<code>🚫 Пароль неверный</code>",
            when=F["is_password"],
        ),
        MessageInput(
            func=password_validate,
            content_types=ContentType.TEXT,
        ),
        Button(
            text=Const("⬅️ Назад"),
            id="btn_back",
            on_click=to_select_mail,
        ),
        state=DelMail.main,
    ),
    Window(
        Jinja(
            text="<b>Удалить почту {{email}}?</b>",
        ),
        Jinja(
            text="<code>🚫 Такой почты не существует</code>",
            when=F["mail_is_none"],
        ),
        Row(
            Button(
                text=Const("❌ Отмена"),
                id="btn_cancel",
                on_click=cancel_delete,
            ),
            Button(
                text=Const("🗑️ Удалить"),
                id="btn_del",
                on_click=del_mail,
            ),
        ),
        state=DelMail.deletion,
    ),
    Window(
        Jinja(
            text="<b>Почта {{email}} удалена ✅</b>",
        ),
        Button(
            text=Const("⬅️ Выйти"),
            id="btn_exit",
            on_click=to_select_mail,
        ),
        state=DelMail.deleted,
    ),
    getter=get_data,
)
