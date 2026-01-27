import asyncio
import email
import logging
import re

from aiogram import Bot
from aiogram.types import CallbackQuery, BufferedInputFile
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
from db.services import ImapService


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


def _get_since_before_criteria(
    year: int,
    month: int,
    day: int
) -> tuple[date, date]:

    since = date(year, month, day)
    month_before = month + 1
    year_before = year

    if month_before > 12:
        month_before = 1
        year_before += 1

    before = date(year_before, month_before, day)

    return since, before


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


async def to_find_mail(
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

    user_id: int = dialog_manager.event.from_user.id
    imap_server: str = dialog_manager.start_data.get("host")
    login: str = dialog_manager.start_data.get("login")
    encrypted_password: str = dialog_manager.start_data.get("password")

    encrypted = SecureEncryptor(user_id)
    password_mail: str = encrypted.decrypted_data(encrypted_password)

    month_name: str = buttons.get(widget.widget_id)
    month_num: int = MONTH_DATA.get(month_name, 1)
    year: int = dialog_manager.dialog_data.get("year")

    since, before = _get_since_before_criteria(
        year=year,
        month=month_num,
        day=1,
    )

    with ImapService(imap_server, login, password_mail) as imap_service:
        client: IMAPClient = imap_service.client
        client.select_folder("INBOX", readonly=True)

        messages: SearchIds = \
            client.search([u"SINCE", since, u"BEFORE", before])

        for uid, message_data in client.fetch(messages, "RFC822").items():
            raw_email: bytes = message_data[b"RFC822"]
            email_message: EmailMessage = email.message_from_bytes(raw_email)

            sender, email_name = imap_service.get_from_email(email_message)

            subject: str = imap_service.get_subject_email(email_message)

            text: str
            attachments: list[tuple[str, bytes]]
            text, attachments = imap_service.get_data_mail(email_message)

            text_message = f"Сообщение от {sender}. Тема: {subject}"
            print(text_message)
            print(f"Текст: {text}")
            print(f"Вложения {attachments}")

            # tasks = []
            # bot: Bot = dialog_manager.event.bot
            # for file_name, attachment in attachments:
            #     file = BufferedInputFile(
            #         file=attachment,
            #         filename=file_name,
            #     )
            #     task = asyncio.create_task(
            #         send_attachment(bot, user_id, file)
            #     )
            #     tasks.append(task)
            # result = await asyncio.gather(
            #     *tasks,
            #     return_exceptions=True,
            # )
            # print(result)

    # await dialog_manager.start(
    #     state=ReadingMail.main,
    #     data=start_data,
    #     mode=StartMode.RESET_STACK,
    #     show_mode=ShowMode.EDIT,
    # )
