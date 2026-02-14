from aiogram import F
from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import (
    Button,
    Select,
    Column,
    ScrollingGroup,
    StubScroll,
    PrevPage,
    NextPage,
    CurrentPage,
    Row,
)
from aiogram_dialog.widgets.text import Const, Format, List, Jinja
from operator import itemgetter

from dialogs.states import SelectLetter
from .getters import (
    get_data,
    get_data_letter,
    get_text_data,
    get_data_attachments,
)
from .handlers import (
    exit_mail,
    on_mail,
    to_main,
    to_read_letter,
    stop_text_read,
    to_read_attachments,
    stop_attachment_read,
    on_attachment,
    send_document,
)


select_letter_dialog = Dialog(
    Window(
        Jinja(
            text="<b>{{period}}</b>",
        ),
        Jinja(
            text="<i>Открываю письмо...</i>",
            when=F["open_letter"],
        ),
        ScrollingGroup(
            Column(
                Select(
                    text=Format('{item[0]}'),
                    id="select_mail",
                    item_id_getter=itemgetter(1),
                    items="select_ids",
                    on_click=on_mail,
                ),
            ),
            id="mail_scroll",
            width=1,
            height=5,
            hide_pager=True,
        ),
        Row(
            PrevPage(
                scroll="mail_scroll",
                text=Const("◀️"),
            ),
            CurrentPage(
                scroll="mail_scroll",
                text=Format("{current_page1} / {pages}"),
            ),
            NextPage(
                scroll="mail_scroll",
                text=Const("▶️"),
            ),
        ),
        Button(
            text=Const("⬅️ Назад"),
            id="btn_exit",
            on_click=exit_mail,
        ),
        getter=get_data,
        state=SelectLetter.main,
    ),
    Window(
        Jinja(
            text="<b>🪪 Отправитель: '{{sender}}'</b>",
        ),
        Jinja(
            text="<b>📢 Тема: '{{subject}}'</b>",
        ),
        Row(
            Button(
                text=Const("📖 Читать"),
                id="btn_to_read",
                on_click=to_read_letter,
            ),
            Button(
                text=Const("🗂️ Вложения"),
                id="btn_to_attachments",
                on_click=to_read_attachments,
                when=F["is_attachments"],
            ),
        ),
        Button(
            text=Const("⬅️ Назад"),
            id="btn_to_main",
            on_click=to_main,
        ),
        getter=get_data_letter,
        state=SelectLetter.letter,
    ),
    Window(
        Jinja(
            text="<b>📄 Текст письма:</b>",
        ),
        List(
            field=Format("{item}"),
            items="pages",
            id="scroll_pages",
            page_size=1,
        ),
        StubScroll(
            id="scroll_pages",
            pages="pages_amount",
        ),
        Row(
            PrevPage(
                scroll="scroll_pages",
                text=Const("◀️"),
            ),
            CurrentPage(
                scroll="scroll_pages",
                text=Format("{current_page1} / {pages}"),
            ),
            NextPage(
                scroll="scroll_pages",
                text=Const("▶️"),
            ),
        ),
        Button(
            text=Const("📩 Отправить текст"),
            id="btn_send_text",
            on_click=send_document,
        ),
        Button(
            text=Const("⬅️ Назад"),
            id="btn_stop_read",
            on_click=stop_text_read,
        ),
        getter=get_text_data,
        state=SelectLetter.text,
    ),
    Window(
        Jinja(
            text="<b>Выбери вложение:</b>",
        ),
        ScrollingGroup(
            Column(
                Select(
                    text=Format('{item[0]}'),
                    id="select_attachment",
                    item_id_getter=itemgetter(1),
                    items="select_attachments",
                    on_click=on_attachment,
                ),
            ),
            id="scroll_attachment",
            width=1,
            height=3,
            hide_pager=True,
        ),
        Row(
            PrevPage(
                scroll="scroll_attachment",
                text=Const("◀️"),
            ),
            CurrentPage(
                scroll="scroll_attachment",
                text=Format("{current_page1} / {pages}"),
            ),
            NextPage(
                scroll="scroll_attachment",
                text=Const("▶️"),
            ),
        ),
        Button(
            text=Const("⬅️ Назад"),
            id="btn_stop_attachment",
            on_click=stop_attachment_read,
        ),
        getter=get_data_attachments,
        state=SelectLetter.attachment,
    ),
)
