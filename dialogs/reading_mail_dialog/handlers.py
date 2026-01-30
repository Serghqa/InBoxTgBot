import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import (
    DialogManager,
    ShowMode,
    StartMode,
)
from aiogram_dialog.widgets.kbd import (
    Button,
    Select,
)

from db.services import ImapService, ImapAuthData, get_imap_auth_data


logger = logging.getLogger(__name__)


async def exit_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.done()


async def on_mail(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str
) -> None:

    imap_auth_data: ImapAuthData = get_imap_auth_data(dialog_manager)
