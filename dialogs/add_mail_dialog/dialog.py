from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Radio, Column, Row
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from operator import itemgetter

from .getters import get_data
from .handlers import (
    add_mail,
    back_to_start_dlg,
    cancel_add_mail,
    input_error,
    input_validate,
    process_start,
    success_login,
    success_password,
)
from states import AddMail


btn_cancel = Button(
    text=Const("Отмена"),
    id="btn_cancel",
    on_click=cancel_add_mail,
)

add_mail_dialog = Dialog(
    Window(
        Format(
            text="Выберите хост почты и введите логин "
                 "почтового ящика.",
        ),
        Column(
            Radio(
                Format(
                    text='☑️ {item[0]}',
                ),
                Format(
                    text='⬜ {item[0]}',
                ),
                id="radio_mail_host",
                item_id_getter=itemgetter(1),
                items="radio",
            ),
        ),
        TextInput(
            id="login",
            type_factory=input_validate,
            on_success=success_login,
            on_error=input_error,
        ),
        Button(
            text=Const("Назад"),
            id="btn_back",
            on_click=back_to_start_dlg,
        ),
        state=AddMail.main,
    ),
    Window(
        Format(
            text="Логин: --{name_mail}--"
        ),
        Format(
            text="Пароль: --Введите пароль--"
        ),
        TextInput(
            id="password",
            type_factory=input_validate,
            on_success=success_password,
            on_error=input_error,
        ),
        btn_cancel,
        state=AddMail.password,
    ),
    Window(
        Format(
            text="Имя почты: --{name_mail}--\n"
                 "Пароль почты: --{password_mail}--",
        ),
        Row(
            Button(
                text=Const("Добавить"),
                id="btn_add_mail",
                on_click=add_mail,
            ),
            btn_cancel,
        ),
        state=AddMail.add_mail,
    ),
    Window(
        Format(
            text="Почта успешно добавлена.",
        ),
        Row(
            Button(
                text=Const("К почте"),
                id="btn_to_mail",
            ),
            Button(
                text=Const("Добавить еще почту"),
                id="btn_add_still_mail",
                on_click=cancel_add_mail,
            ),
        ),
        state=AddMail.success_mail,
    ),
    getter=get_data,
    on_start=process_start,
)
