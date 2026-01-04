from .models import (
    Base,
    User,
)


def set_user(
    user_id: int,
    name: str
) -> User:

    return User(
        user_id=user_id,
        name=name,
    )


__all__ = [
    Base,
    User,
    set_user,
]
