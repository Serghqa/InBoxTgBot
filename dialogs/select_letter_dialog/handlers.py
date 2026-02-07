import asyncio
import email
import logging

from aiogram.types import CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from aiogram_dialog import (
    DialogManager,
    ShowMode,
)
from aiogram_dialog.widgets.kbd import (
    Button,
    Select,
)
from aiogram_dialog.widgets.common.scroll import ManagedScroll
from aiogram.types import BufferedInputFile
from email.message import Message as EmailMessage
from imapclient import IMAPClient

from db.services import (
    ImapService,
    ImapAuthData,
    SecureEncryptor,
    get_imap_auth_data,
)
from dialogs.states import SelectLetter


logger = logging.getLogger(__name__)


def _fetch_text_attachment(
    imap_auth_data: ImapAuthData,
    uid: int,
    password: str
) -> tuple[str, list[tuple[str, bytes]]]:

    with ImapService(
        imap_auth_data.imap_server,
        imap_auth_data.login,
        password,
    ) as imap_service:
        client: IMAPClient = imap_service.client
        client.select_folder("INBOX", readonly=True)
        raw_data = client.fetch([uid], ["RFC822"])
        message_bytes = raw_data[uid][b"RFC822"]
        message: EmailMessage = email.message_from_bytes(message_bytes)

        text, attachments = imap_service.get_data_email(message)

        return text, attachments


async def exit_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.done()


async def to_main(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    dialog_manager.dialog_data.clear()

    await dialog_manager.switch_to(
        state=SelectLetter.main,
        show_mode=ShowMode.EDIT,
    )


async def stop_text_read(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    scroll: ManagedScroll = dialog_manager.find("scroll_pages")
    await scroll.set_page(0)

    await dialog_manager.switch_to(
        state=SelectLetter.letter,
        show_mode=ShowMode.EDIT,
    )


async def stop_attachment_read(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    scroll: ManagedScroll = dialog_manager.find("scroll_attachment")
    await scroll.set_page(0)

    await dialog_manager.switch_to(
        state=SelectLetter.letter,
        show_mode=ShowMode.EDIT,
    )


async def on_attachment(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str
) -> None:

    attachments: list[tuple[str, bytes]] = \
        dialog_manager.dialog_data.get("attachments")
    filename, payload = attachments[int(item_id)]

    async with ChatActionSender.upload_document(
        bot=callback.bot,
        chat_id=callback.message.chat.id,
    ):
        file_to_send = BufferedInputFile(
            file=payload,
            filename=filename,
        )
        try:
            await callback.message.answer_document(
                document=file_to_send,
                caption=f"Файл: {filename}"
            )
        except Exception:
            logger.error(
                "Ошибка при отправке файла",
                exc_info=True,
            )
            await callback.message.answer(
                text=f"Не удалось отправить файл {filename}",
            )


async def to_read_letter(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    text: str = dialog_manager.dialog_data.get("text")
    if not text:
        await callback.answer(
            text="Письмо без текста",
        )
        return

    await dialog_manager.switch_to(
        state=SelectLetter.text,
        show_mode=ShowMode.EDIT,
    )


async def to_read_attachments(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    attachments: list[tuple[str, bytes]] = \
        dialog_manager.dialog_data.get("attachments")
    if not attachments:
        await callback.answer(
            text="Письмо без вложений",
        )
        return

    await dialog_manager.switch_to(
        state=SelectLetter.attachment,
        show_mode=ShowMode.EDIT,
    )


async def on_mail(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str
) -> None:

    await callback.answer(
        text="Подождите, загружаю данные письма...",
    )
    uid = int(item_id)

    imap_auth_data: ImapAuthData = get_imap_auth_data(dialog_manager)

    encrypted = SecureEncryptor(imap_auth_data.user_id)
    password_mail: str = \
        encrypted.decrypted_data(imap_auth_data.encrypted_password)

    try:
        text, attachments = await asyncio.to_thread(
            _fetch_text_attachment,
            imap_auth_data,
            uid,
            password_mail,
        )

        dialog_manager.dialog_data["text"] = text
        dialog_manager.dialog_data["attachments"] = attachments
        dialog_manager.dialog_data["uid"] = uid

        await dialog_manager.switch_to(
            state=SelectLetter.letter,
            show_mode=ShowMode.EDIT,
        )
    except Exception:
        logger.error(
            "Ошибка при получении данных письма",
            exc_info=True
        )
        await callback.message.answer(
            text="Не удалось загрузить содержимое письма."
        )
