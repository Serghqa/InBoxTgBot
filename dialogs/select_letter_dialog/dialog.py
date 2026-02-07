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
from aiogram_dialog.widgets.text import Const, Format, List
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
)


select_letter_dialog = Dialog(
    Window(
        Format(
            text="{period}",
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
                text=Const("⬅️"),
            ),
            CurrentPage(
                scroll="mail_scroll",
                text=Format("{current_page1} / {pages}"),
            ),
            NextPage(
                scroll="mail_scroll",
                text=Const("➡️"),
            ),
        ),
        Button(
            text=Const("Назад"),
            id="btn_exit",
            on_click=exit_mail,
        ),
        getter=get_data,
        state=SelectLetter.main,
    ),
    Window(
        Format(
            text="Отправитель: '{sender}'",
        ),
        Format(
            text="Тема: '{subject}'",
        ),
        Row(
            Button(
                text=Const("Читать"),
                id="btn_to_read",
                on_click=to_read_letter,
            ),
            Button(
                text=Const("Вложения"),
                id="btn_to_attachments",
                on_click=to_read_attachments,
            ),
        ),
        Button(
            text=Const("Назад"),
            id="btn_to_main",
            on_click=to_main,
        ),
        getter=get_data_letter,
        state=SelectLetter.letter,
    ),
    Window(
        Format(
            text="Текст письма:",
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
                text=Const("⬅️"),
            ),
            CurrentPage(
                scroll="scroll_pages",
                text=Format("{current_page1} / {pages}"),
            ),
            NextPage(
                scroll="scroll_pages",
                text=Const("➡️"),
            ),
        ),
        Button(
            text=Const("Назад"),
            id="btn_stop_read",
            on_click=stop_text_read,
        ),
        getter=get_text_data,
        state=SelectLetter.text,
    ),
    Window(
        Format(
            text="Выбери вложение:",
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
                text=Const("⬅️"),
            ),
            CurrentPage(
                scroll="scroll_attachment",
                text=Format("{current_page1} / {pages}"),
            ),
            NextPage(
                scroll="scroll_attachment",
                text=Const("➡️"),
            ),
        ),
        Button(
            text=Const("Назад"),
            id="btn_stop_attachment",
            on_click=stop_attachment_read,
        ),
        getter=get_data_attachments,
        state=SelectLetter.attachment,
    ),
)

# START_DATA={
#     'login': 'psl.ru@mail.ru',
#     'host': 'imap.mail.ru',
#     'password': 'gAAAAABpeyTYtu486JdTGXeMOWLSYS5IsNMfkalhY-CYlgxJ14n8GaqFhiIiObGUISOt03LXWTRjsuIHhsRa5I2UIv3yIfIsAikQ6zSJ0EzlfbhocwyU46Y=',
#     'date': 'Январь 2026',
#     'messages': {
#         58918: {'date': '2026-01-20', 'sender': 'Фонд капитального ремонта Пермского края', 'subject': 'Квитанция за январь 2026г.'},
#         58920: {'date': '2026-01-21', 'sender': 'Google Play', 'subject': 'Мы изменили настройки конфиденциальности для Google Play'},
#         58925: {'date': '2026-01-27', 'sender': 'ООО "Газпром межрегионгаз Пермь"', 'subject': 'Электронный платежный документ за январь 2026г.'},
#         58929: {'date': '2026-01-28', 'sender': 'Территория партнерства', 'subject': 'Солдатова_24_191_012026.pdf'}
#     }
# }
# DIALOG_DATA={}
# WIDGET_DATA={}
# STATE=<State 'ReadingMail:main'>
