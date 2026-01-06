from .models import (
    Base,
    User,
    ImapCredentials,
)


def set_user(user_id: int) -> User:

    return User(user_id=user_id)


def set_imap_credentials(
    email: str,
    password: str,
    imap_server: str,
    user_id: int
) -> ImapCredentials:

    return ImapCredentials(
        email=email,
        password=password,
        imap_server=imap_server,
        user_id=user_id,
    )


__all__ = [
    Base,
    User,
    ImapCredentials,
    set_user,
    set_imap_credentials
]
