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
)
from email.header import decode_header
from email.message import Message as EmailMessage
from email.utils import parseaddr
from datetime import datetime, date
from imapclient import IMAPClient
from imapclient.response_types import SearchIds
from zoneinfo import ZoneInfo

from dialogs.states import StartSG, Mail, ReadingMail
from db.services import SecureEncryptor


logger = logging.getLogger(__name__)


buttons = {
    "btn_january": "Январь",
    "btn_february": "Февраль",
    "btn_march": "Март",
    "btn_april": "Апрель",
    "btn_may": "Май",
    "btn_june": "Июнь",
    "btn_jule": "Июль",
    "btn_august": "Август",
    "btn_september": "Сентябрь",
    "btn_october": "Октябрь",
    "btn_november": "Ноябрь",
    "btn_december": "Декабрь",
}

MONTH_DATA = {
    "Январь": 1, "Февраль": 2, "Март": 3, "Апрель": 4,
    "Май": 5, "Июнь": 6, "Июль": 7, "Август": 8,
    "Сентябрь": 9, "Октябрь": 10, "Ноябрь": 11, "Декабрь": 12,
}


def _parse_data(
    data: list[tuple[bytes, str | None]],
    default_content: str,
    charset="utf-8"
) -> str:

    content = default_content

    raw_content: bytes | str
    charset: str | None
    raw_content, charset = data[0]

    if isinstance(raw_content, bytes):
        content = raw_content.decode(charset or "utf-8")
    elif isinstance(raw_content, str) and len(raw_content) > 0:
        content = raw_content

    return content


def _get_from_email(message: EmailMessage) -> tuple[str, str]:

    message = message.get("From")
    sender_email, name_email = parseaddr(message)
    result: list[tuple[bytes, str | None]] = decode_header(sender_email)

    if not result:
        return "", ""

    sender: str = _parse_data(
        data=result,
        default_content="Без имени",
    )

    return sender, name_email


def _get_subject_email(message: EmailMessage) -> str:

    message = message.get("Subject")
    result: list[tuple[bytes, str | None]] = decode_header(message)

    if not result:
        return ""

    subject: str = _parse_data(
        data=result,
        default_content="Без темы",
    )

    return subject


async def exit_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.start(
        state=StartSG.main,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
    )


async def to_find_receipts(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.switch_to(
        state=Mail.calendar,
        show_mode=ShowMode.EDIT,
    )


async def to_main(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.switch_to(
        state=Mail.main,
        show_mode=ShowMode.EDIT,
    )


async def shift_year(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    tz = ZoneInfo("Asia/Yekaterinburg")
    today = datetime.now(tz)

    year: int = dialog_manager.dialog_data.get("year", today.year)
    if widget.widget_id == "btn_prev":
        year -= 1
    if widget.widget_id == "btn_next":
        year += 1

    dialog_manager.dialog_data["year"] = year


async def process_clicked(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    month_name: str = buttons.get(widget.widget_id)
    month_num: int = MONTH_DATA.get(month_name, 1)
    year: int = dialog_manager.dialog_data.get("year")

    since = date(year, month_num, 1)
    month_before = month_num + 1
    year_before = year
    if month_before > 12:
        month_before = 1
        year_before += 1
    before = date(year_before, month_before, 1)

    user_id: int = dialog_manager.event.from_user.id
    imap_server: str = dialog_manager.start_data.get("host")
    login: str = dialog_manager.start_data.get("login")
    encrypted_password: str = dialog_manager.start_data.get("password")

    encrypted = SecureEncryptor(user_id)
    password_mail: str = encrypted.decrypted_data(encrypted_password)

    with IMAPClient(imap_server, use_uid=True,) as server:
        server.login(login, password_mail)
        server.select_folder("INBOX", readonly=True)

        messages: SearchIds = \
            server.search([u"SINCE", since, u"BEFORE", before])

        for uid, message_data in server.fetch(messages, "RFC822").items():
            raw_email: bytes = message_data[b"RFC822"]
            email_message: EmailMessage = email.message_from_bytes(raw_email)
            sender, email_name = _get_from_email(email_message)
            print(f"От {sender}: {email_name}")
            subject = _get_subject_email(email_message)
            print(f"Тема: {subject}")

            # subject_message = email_message.get("Subject")

    # await dialog_manager.start(
    #     state=ReadingMail.main,
    #     data=start_data,
    #     mode=StartMode.RESET_STACK,
    #     show_mode=ShowMode.EDIT,
    # )
