from aiogram_dialog import DialogManager
from dataclasses import dataclass
from datetime import datetime
from email.header import decode_header, make_header
from email.message import Message
from email.utils import parseaddr
from imapclient import IMAPClient
from imapclient.response_types import SearchIds


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

        message = email_message.get("Subject")
        result: list[tuple[bytes, str | None]] = decode_header(message)

        if not result:
            return ""

        subject: str = self._parse_data(
            data=result,
            default_content="Без темы",
        )

        return subject

    def get_from_email(
        self,
        email_message: Message
    ) -> tuple[str, str]:

        message = email_message.get("From")
        sender_email, name_email = parseaddr(message)
        result: list[tuple[bytes, str | None]] = decode_header(sender_email)

        if not result:
            return "", ""

        sender: str = self._parse_data(
            data=result,
            default_content="Без имени",
        )

        return sender, name_email

    def _parse_data(
        self,
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

    def get_data_email(
        self,
        message: Message
    ) -> tuple[str, list[tuple[str, bytes]]]:

        attachments = []
        texts = []

        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = \
                    str(part.get_content_disposition()).lower()

                if (
                    content_type == "text/plain"
                    and "attachment" not in content_disposition
                ):
                    paylod = part.get_payload(decode=True)
                    charset = part.get_content_charset() or "utf-8"
                    text: str = paylod.decode(charset, errors="ignore")

                    texts.append(text)

                elif "attachment" in content_disposition:
                    raw_filename = part.get_filename()
                    filename = str(make_header(decode_header(raw_filename)))

                    payload_bytes = part.get_payload(decode=True)

                    if filename and payload_bytes:
                        attachments.append((filename, payload_bytes))
        else:
            content_type = message.get_content_type()
            if content_type == "text/plain":
                payload = message.get_payload(decode=True)
                charset = message.get_content_charset() or "utf-8"
                text: str = payload.decode(charset)
                texts.append(text)

        if not texts:
            texts.append("Без текста")

        result_text = "\n".join(texts)

        return result_text, attachments

    def get_internaldate_messages(
        self,
        ids_messages: SearchIds
    ) -> dict[int, datetime]:

        response = self.client.fetch(ids_messages, ["INTERNALDATE"])

        return {
            ids: data[b"INTERNALDATE"] for ids, data in response.items()
        }
