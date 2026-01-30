import asyncio
import email
import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import (
    DialogManager,
    ShowMode,
    StartMode,
    Data,
)
from aiogram_dialog.widgets.kbd import (
    Button,
    Select,
)
from aiogram_dialog.api.internal import RawKeyboard
from collections import Counter
from babel.dates import get_month_names
from email.message import Message as EmailMessage
from datetime import datetime, date
from imapclient import IMAPClient
from imapclient.response_types import SearchIds
from zoneinfo import ZoneInfo

from dialogs.states import StartSG, Mail, SelectLetter
from db.services import SecureEncryptor
from db.services import ImapService, ImapAuthData, get_imap_auth_data


logger = logging.getLogger(__name__)


RU_MONTHS = [
    "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
]


class CustomSelect(Select):

    async def _render_keyboard(
        self,
        data: dict,
        manager: DialogManager,
    ) -> RawKeyboard:

        keyboard = []
        row = []

        for pos, item in enumerate(self.items_getter(data)):
            row.append(
                await self._render_button(pos, item, item, data, manager)
            )
            if len(row) == 4:
                keyboard.append(row)
                row = []

        return keyboard


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


def _count_messages(data: dict[int, datetime]) -> list[int]:

    counts = Counter(dt.month for dt in data.values())
    monthy_counts = [counts.get(month, 0) for month in range(1, 13)]

    return monthy_counts


def _get_data_messages(
    imap_auth_data: ImapAuthData,
    interval: tuple[date, date],
    month_messages: list[int]
) -> dict:

    result_data = {}

    since, before = interval
    encrypted = SecureEncryptor(imap_auth_data.user_id)
    password_mail: str = \
        encrypted.decrypted_data(imap_auth_data.encrypted_password)

    with ImapService(
        imap_auth_data.imap_server,
        imap_auth_data.login,
        password_mail,
    ) as imap_service:
        client: IMAPClient = imap_service.client
        client.select_folder("INBOX", readonly=True)

        ids_messages: SearchIds = \
            client.search(["SINCE", since, "BEFORE", before])

        if month_messages != len(ids_messages):
            raise ValueError

        if not ids_messages:
            return result_data

        for uid, message_data in client.fetch(
            ids_messages,
            ["RFC822.HEADER", "INTERNALDATE"]
        ).items():
            message_bytes: bytes = message_data[b"RFC822.HEADER"]
            email_message: EmailMessage = \
                email.message_from_bytes(message_bytes)

            sender, email_name = imap_service.get_from_email(email_message)
            subject: str = imap_service.get_subject_email(email_message)
            message_dt: datetime = message_data.get(b"INTERNALDATE")

            result_data[uid] = {
                "date": message_dt.date().isoformat(),
                "sender": sender,
                "subject": subject,
            }

    return result_data


def _fetch_imap_counts(
    imap_auth_data: ImapAuthData,
    password: str,
    since: date,
    before: date
) -> list[int]:

    with ImapService(
        imap_auth_data.imap_server,
        imap_auth_data.login,
        password,
    ) as imap_service:
        client: IMAPClient = imap_service.client
        client.select_folder("INBOX", readonly=True)
        ids_messages: SearchIds = \
            client.search(["SINCE", since, "BEFORE", before])
        internaldate_msg: dict[int, datetime] = \
            imap_service.get_internaldate_messages(ids_messages)
        monthy_counts: list[int] = _count_messages(internaldate_msg)

        return monthy_counts


def _get_months_abbr(dialog_manager: DialogManager) -> list[str]:

    months_abbr: list[str] = \
        dialog_manager.dialog_data.get("months_abbr")
    if months_abbr is None:
        months_dict = \
            get_month_names("abbreviated", locale="ru", context="stand-alone")
        months_abbr = [
            months_dict[i].replace('.', '').capitalize() for i in range(1, 13)
        ]

    return months_abbr


async def _update_calendar_data(dialog_manager: DialogManager) -> None:

    months_abbr: list[str] = _get_months_abbr(dialog_manager)
    dialog_manager.dialog_data["months_abbr"] = months_abbr

    imap_auth_data: ImapAuthData = get_imap_auth_data(dialog_manager)

    year: int = dialog_manager.dialog_data.get("year")

    encrypted = SecureEncryptor(imap_auth_data.user_id)
    password_mail: str = \
        encrypted.decrypted_data(imap_auth_data.encrypted_password)

    since, before = date(year, 1, 1), date(year+1, 1, 1)

    monthy_counts: list[int] = await asyncio.to_thread(
        _fetch_imap_counts,
        imap_auth_data,
        password_mail,
        since,
        before,
    )
    dialog_manager.dialog_data["messages"] = monthy_counts


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

    try:
        await _update_calendar_data(dialog_manager)
    except Exception:
        logger.error(
            "Ошибка обновления данных календаря",
            exc_info=True,
        )
        await callback.answer(
            text="Не получилось, попробуй еще раз",
            show_alert=True,
        )
        return

    await dialog_manager.switch_to(
        state=Mail.calendar,
        show_mode=ShowMode.EDIT,
    )


async def to_main(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    dialog_manager.dialog_data.clear()

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
    old_year = year
    if widget.widget_id == "btn_prev":
        year -= 1
    if widget.widget_id == "btn_next":
        year += 1

    dialog_manager.dialog_data["year"] = year
    try:
        await _update_calendar_data(dialog_manager)
    except Exception:
        logger.error(
            "Ошибка обновления данных календаря",
            exc_info=True,
        )
        await callback.answer(
            text="Не получилось, попробуй еще раз",
            show_alert=True,
        )
        dialog_manager.dialog_data["year"] = old_year


async def process_clicked(
    callback: CallbackQuery,
    widget: CustomSelect,
    dialog_manager: DialogManager,
    item_id: str
) -> None:

    imap_auth_data: ImapAuthData = get_imap_auth_data(dialog_manager)

    month_item: int = int(item_id)
    year: int = dialog_manager.dialog_data.get("year")

    since, before = _get_since_before_criteria(
        year=year,
        month=month_item,
        day=1,
    )
    old_messages: list[int] = dialog_manager.dialog_data.get("messages")
    month_messages: int = old_messages[month_item-1]

    try:
        result_data: dict = await asyncio.to_thread(
            _get_data_messages,
            imap_auth_data,
            (since, before),
            month_messages,
        )

        if not result_data:
            await callback.answer(
                text="В выбранном месяце нет писем",
                show_alert=True,
            )

            return

        start_data = {}
        start_data.update(dialog_manager.start_data)
        start_data["messages"] = result_data
        start_data["period"] = \
            f"{RU_MONTHS[since.month-1]} {since.strftime('%Y')}"

        await dialog_manager.start(
            state=SelectLetter.main,
            data=start_data,
            show_mode=ShowMode.EDIT,
        )
    except ValueError:
        await callback.answer(
            text="Данные о сообщениях были изменены",
            show_alert=True,
        )
    except Exception:
        logger.error(
            "Ошибка извлечения данных из писем",
            exc_info=True,
        )
        await callback.answer(
            text="Не удалось получить ваши письма, попробуйте еще раз",
            show_alert=True,
        )


async def process_result(
    start_data: Data,
    result: dict,
    dialog_manager: DialogManager
) -> None:

    try:
        await _update_calendar_data(dialog_manager)
    except Exception:
        logger.error(
            "Ошибка обновления данных календаря",
            exc_info=True,
        )
        await dialog_manager.event.answer(
            text="Не удалось загрузить список писем",
            show_alert=True,
        )
        months_abbr: list[str] = _get_months_abbr(dialog_manager)
        dialog_manager.dialog_data["months_abbr"] = months_abbr

        dialog_manager.dialog_data["messages"] = [0] * 12
