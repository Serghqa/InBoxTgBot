import email

from imapclient import IMAPClient
from email.utils import parseaddr

addresses = [
    "no-reply.perm@epd.online",
    "pismo@novogor.perm.ru",
    "BigBilling@energos.perm.ru",
    "invoice@krc-prikam.ru",
    "no-reply.perm@epd.online",
]


with IMAPClient("imap.mail.ru", use_uid=True) as server:
    server.login("psl.ru@mail.ru", "eW6EeYMjoNA9tO3MNnAT")
    select_info = server.select_folder("Квитанции", readonly=True)

    messages = server.search()

    for uid, message_data in server.fetch(messages, "RFC822").items():
        raw_email = message_data[b"RFC822"]
        email_message = email.message_from_bytes(raw_email)

        from_header = email_message.get("From")
        _, sender_email = parseaddr(from_header)
        print(sender_email)
