from aiogram_dialog import (
    Dialog,
    Window,
)
from aiogram_dialog.widgets.kbd import Button, Select, Column
from aiogram_dialog.widgets.text import Const, Format
from operator import itemgetter

from dialogs.states import SelectLetter
from .getters import get_data
from .handlers import exit_mail, on_mail


select_letter_dialog = Dialog(
    Window(
        Format(
            text="{period}",
        ),
        Column(
            Select(
                text=Format('{item[0]}'),
                id="select_mail",
                item_id_getter=itemgetter(1),
                items="select_ids",
                on_click=on_mail,
            ),
        ),
        Button(
            text=Const("Назад"),
            id="btn_back",
            on_click=exit_mail,
        ),
        getter=get_data,
        state=SelectLetter.main,
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
