import email
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
from email.message import Message as EmailMessage
from imapclient import IMAPClient

from db.services import (
    ImapService,
    ImapAuthData,
    SecureEncryptor,
    get_imap_auth_data,
)


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

    uid = int(item_id)

    imap_auth_data: ImapAuthData = get_imap_auth_data(dialog_manager)

    encrypted = SecureEncryptor(imap_auth_data.user_id)
    password_mail: str = \
        encrypted.decrypted_data(imap_auth_data.encrypted_password)

    with ImapService(
        imap_auth_data.imap_server,
        imap_auth_data.login,
        password_mail
    ) as imap_service:
        client: IMAPClient = imap_service.client
        client.select_folder("INBOX", readonly=True)
        raw_data = client.fetch([uid], ["RFC822"])
        message_bytes = raw_data[uid][b"RFC822"]
        message: EmailMessage = email.message_from_bytes(message_bytes)

        text, _ = imap_service.get_data_email(message)
