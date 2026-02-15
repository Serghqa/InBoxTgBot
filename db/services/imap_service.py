from aiogram_dialog import DialogManager
from base64 import b64encode
from dataclasses import dataclass
from datetime import datetime
from email.header import decode_header, make_header
from email.message import Message
from email.utils import parseaddr
from imapclient import IMAPClient
from imapclient.response_types import SearchIds
from typing import TypeAlias


Base64String: TypeAlias = str


@dataclass
class ImapAuthData:

    user_id: int
    imap_server: str
    login: str
    encrypted_password: str


def get_imap_auth_data(dialog_manager: DialogManager) -> ImapAuthData:

    user_id: int = dialog_manager.event.from_user.id
    imap_server: str = dialog_manager.start_data.get("host")
    login: str = dialog_manager.start_data.get("login")
    encrypted_password: str = dialog_manager.start_data.get("password")

    return ImapAuthData(
        user_id=user_id,
        imap_server=imap_server,
        login=login,
        encrypted_password=encrypted_password,
    )


class ImapService:

    def __init__(
        self,
        imap_server: str,
        login: str,
        password: str,
        use_uid: bool = True
    ) -> None:

        self.imap_server = imap_server
        self.login = login
        self.use_uid = use_uid
        self.client: IMAPClient | None = None
        self._password = password
        self._is_connected = False

    def __enter__(self) -> "ImapService":

        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:

        self._disconnect()

    def _connect(self) -> "ImapService":

        if self._is_connected:
            return self

        try:
            self.client = IMAPClient(
                self.imap_server,
                use_uid=self.use_uid,
            )
            self.client.login(self.login, self._password)
            self._is_connected = True
            return self

        except Exception as error:
            self._is_connected = False
            raise ConnectionError(
                f"Ошибка соединения с сервером {error}"
            )

    def _disconnect(self) -> None:

        if self.client and self._is_connected:
            try:
                self.client.logout()

            except Exception as error:
                raise ConnectionError(
                    f"Ошибка отключения от сервера {error}"
                )

            finally:
                self.client = None
                self._is_connected = False

    def get_subject_email(
        self,
        email_message: Message
    ) -> str:

        subject_default = "Без темы"

        message = email_message.get("Subject")
        if not message:
            return subject_default

        result: list[tuple[bytes, str | None]] = decode_header(message)

        if not result:
            return subject_default

        subject: str = self._parse_data(
            data=result,
            default_content=subject_default,
        )

        return subject

    def get_from_email(
        self,
        email_message: Message
    ) -> tuple[str, str]:

        message = email_message.get("From")
        if not message:
            return "Без имени", "Неизвестный адрес"

        name_raw, address = parseaddr(message)
        name_parts = decode_header(name_raw)
        sender_name: str = self._parse_data(
            data=name_parts,
            default_content="Без имени",
        )

        return sender_name, address

    def _parse_data(
        self,
        data: list[tuple[bytes, str | None]],
        default_content: str
    ) -> str:

        parts = []

        for raw_content, charset in data:
            if isinstance(raw_content, bytes):
                decoded_part = \
                    raw_content.decode(charset or "utf-8", errors="replace")
                parts.append(decoded_part)
            elif isinstance(raw_content, str):
                parts.append(raw_content)

        content = "".join(parts).strip()

        return content if content else default_content

    def get_data_email(
        self,
        message: Message
    ) -> tuple[str, list[tuple[str, Base64String]]]:

        attachments = []
        texts = []

        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = \
                str(part.get_content_disposition()).lower()
            if (
                content_type == "text/plain"
                and "attachment" not in content_disposition
            ):
                paylod = part.get_payload(decode=True)
                if paylod:
                    charset = part.get_content_charset() or "utf-8"
                    text: str = paylod.decode(charset, errors="replace")
                    texts.append(text)
            elif "attachment" in content_disposition or part.get_filename():
                raw_filename = part.get_filename()
                if raw_filename:
                    filename = str(make_header(decode_header(raw_filename)))
                else:
                    filename = f"attachment_{len(attachments) + 1}"
                payload_bytes = part.get_payload(decode=True)
                if payload_bytes:
                    b64_str = b64encode(payload_bytes).decode("utf8")
                    attachments.append((filename, b64_str))

        result_text = "\n".join(texts).strip()
        if not result_text:
            result_text = "Без текста"

        return result_text, attachments

    def get_internaldate_messages(
        self,
        ids_messages: SearchIds
    ) -> dict[int, datetime]:

        response = self.client.fetch(ids_messages, ["INTERNALDATE"])

        return {
            ids: data[b"INTERNALDATE"] for ids, data in response.items()
        }
