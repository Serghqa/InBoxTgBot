import logging

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import (
    Data,
    DialogManager,
    ShowMode,
    StartMode,
)
from aiogram_dialog.api.entities.context import Context
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput
from email_validator import validate_email, EmailNotValidError
from imapclient import IMAPClient
from imapclient.exceptions import IMAPClientError, LoginError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from dialogs.states import StartSG


logger = logging.getLogger(__name__)


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
