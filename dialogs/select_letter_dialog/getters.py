import textwrap

from aiogram_dialog import DialogManager
from html import escape


def _get_pages(text: str) -> list[str]:

    MAX_SIZE = 1000

    return [
        escape(page) for page in textwrap.wrap(
            text,
            width=MAX_SIZE,
            drop_whitespace=True,
            replace_whitespace=False,
            break_long_words=False,
            break_on_hyphens=False,
        )
    ]


def _truncate_sender(sender: str, max_length: int = 25) -> str:

    if len(sender) <= max_length:
        return sender

    return f"{sender[:max_length-10]}...{sender[-7:]}"


async def get_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:

    messages: dict = dialog_manager.start_data.get("messages")

    select_ids = [
        (_truncate_sender(data["sender"]), ids)
        for ids, data in messages.items()
    ]
    str_period: str = dialog_manager.start_data.get("period")
    return {
        "select_ids": select_ids,
        "period": str_period,
    }


async def get_data_attachments(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:

    attachments: list[tuple[str, bytes]] = \
        dialog_manager.dialog_data["attachments"]
    select_attachments = [
        (data[0], item) for item, data in enumerate(attachments)
    ]

    return {
        "select_attachments": select_attachments,
    }


async def get_data_letter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:

    uid: int = dialog_manager.dialog_data["uid"]
    message: dict = dialog_manager.start_data["messages"][uid]

    data = {}

    data["sender"] = message["sender"]
    data["subject"] = message["subject"]

    return data


async def get_text_data(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:

    data = {}

    text: str = dialog_manager.dialog_data["text"]
    pages: list[str] = _get_pages(text)
    data["pages"] = pages
    data["pages_amount"] = len(pages)

    return data
