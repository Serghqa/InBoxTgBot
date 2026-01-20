from .start_dialog import start_router, start_dialog
from .add_mail_dialog import add_mail_dialog
from .select_mail_dialog import select_mail_dialog
from .mail_dialog import mail_dialog
from .del_mail_dialog import del_mail_dialog
from .reading_mail_dialog import reading_mail_dialog
from .password_mail_dialog import password_mail_dialog


routers = [
    start_router,
    start_dialog,
    add_mail_dialog,
    select_mail_dialog,
    mail_dialog,
    del_mail_dialog,
    reading_mail_dialog,
    password_mail_dialog,
]

__all__ = [
    routers,
]
