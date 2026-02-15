from aiogram import F
from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Radio, Column, Row
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format, Jinja
from operator import itemgetter

from .getters import get_data, get_data_mail, get_login
from .handlers import (
    add_mail,
    back_to_start_dlg,
    cancel_add_mail,
    login_error,
    password_error,
    login_validate,
    password_validate,
    process_start,
    success_login,
    success_password,
    to_mail,
    to_login,
)
from dialogs.states import AddMail


btn_cancel = Button(
    text=Const("❌ Отмена"),
    id="btn_cancel",
    on_click=cancel_add_mail,
)

add_mail_dialog = Dialog(
    Window(
        Jinja(
            text="<b>💬 Выбери хост почты</b>",
        ),
        Column(
            Radio(
                Format(
                    text="☑️ {item[0]}",
                ),
                Format(
                    text="⬜ {item[0]}",
                ),
                id="radio_mail_host",
                item_id_getter=itemgetter(1),
                items="radio",
            ),
        ),
        Row(
            Button(
                text=Const("⬅️ Назад"),
                id="btn_back",
                on_click=back_to_start_dlg,
            ),
            Button(
                text=Const("➡️ Дальше"),
                id="btn_to_login",
                on_click=to_login,
            ),
        ),
        state=AddMail.main,
    ),
    Window(
        Jinja(
            text="<b>💬 Отправь логин</b>",
        ),
        Jinja(
            text="<code>🚫 Недопустимый формат логина</code>",
            when=F["login_err"],
        ),
        TextInput(
            id="login",
            type_factory=login_validate,
            on_success=success_login,
            on_error=login_error,
        ),
        btn_cancel,
        state=AddMail.login,
    ),
    Window(
        Jinja(
            text="<b>💬 Отправь пароль</b>"
        ),
        Jinja(
            text="Логин: <tg-spoiler>{{login}} ✅</tg-spoiler>",
        ),
        Jinja(
            text="<code>🚫 Недопустимый формат пароля</code>",
            when=F["password_err"],
        ),
        Jinja(
            text="<code>🚫 Неверный логин или пароль</code>",
            when=F['auth_err'],
        ),
        TextInput(
            id="password",
            type_factory=password_validate,
            on_success=success_password,
            on_error=password_error,
        ),
        btn_cancel,
        getter=get_login,
        state=AddMail.password,
    ),
    Window(
        Jinja(
            text="Логин: <tg-spoiler>{{name_mail}} ✅</tg-spoiler>",
        ),
        Jinja(
            text="Пароль: <tg-spoiler>{{password_mail}} ✅</tg-spoiler>",
        ),
        Jinja(
            text="<b>💬 Эта почта была добавлена ранее</b>",
            when=F["is_mail"],
        ),
        Row(
            Button(
                text=Const("🆗 Добавить"),
                id="btn_add_mail",
                on_click=add_mail,
            ),
            btn_cancel,
        ),
        getter=get_data_mail,
        state=AddMail.add_mail,
    ),
    Window(
        Jinja(
            text="<b>Почта успешно добавлена ✅</b>",
        ),
        Row(
            Button(
                text=Const("↗️ К почте"),
                id="btn_to_mail",
                on_click=to_mail,
            ),
            Button(
                text=Const("🔄 Добавить еще"),
                id="btn_add_still_mail",
                on_click=cancel_add_mail,
            ),
        ),
        state=AddMail.success_mail,
    ),
    getter=get_data,
    on_start=process_start,
)
