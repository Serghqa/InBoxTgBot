from .start_dialog import start_router, start_dialog
from .add_mail_dialog import add_mail_dialog
from .select_mail_dialog import select_mail_dialog


routers = [
    start_router,
    start_dialog,
    add_mail_dialog,
    select_mail_dialog,
]

__all__ = [
    routers,
]
