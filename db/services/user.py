import bcrypt

from sqlalchemy import select

from db.services import DAO
from db.models import (
    User,
    ImapCredentials,
    set_user,
    set_imap_credentials,
)


class UserDAO(DAO):

    async def get_user(self) -> User | None:

        user: User | None = await self.session.get(User, self.user_id)

        return user

    async def add_user(self) -> User:

        user: User = set_user(self.user_id)

        self.session.add(user)
        await self.session.commit()

        return user

    async def add_imap_credentials(
        self,
        email: str,
        password: str,
        imap_server: str
    ) -> ImapCredentials:

        imap_credentials: ImapCredentials = set_imap_credentials(
            email=email,
            password=password,
            imap_server=imap_server,
            user_id=self.user_id,
        )
        self.session.add(imap_credentials)
        await self.session.commit()

        return imap_credentials

    async def get_imap_credentials(
        self,
        email: str,
        imap_server: str
    ) -> ImapCredentials | None:

        stmt = (
            select(ImapCredentials)
            .where(
                ImapCredentials.email == email,
                ImapCredentials.imap_server == imap_server,
                ImapCredentials.user_id == self.user_id
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar()

    async def get_user_credentials(self) -> list[ImapCredentials]:

        stmt = (
            select(ImapCredentials)
            .where(
                ImapCredentials.user_id == self.user_id,
            )
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()

    def generate_hash(self, password: str) -> str:

        password_bytes: bytes = password.encode("utf-8")
        password_salt: bytes = bcrypt.gensalt()
        hash_bytes: bytes = bcrypt.hashpw(password_bytes, password_salt)
        hash_str: str = hash_bytes.decode("utf-8")

        return hash_str

    def authenticate(self, password: str, hash_str: str) -> bool:

        password_bytes: bytes = password.encode("utf-8")
        hash_bytes: bytes = hash_str.encode("utf-8")
        result: bool = bcrypt.checkpw(password_bytes, hash_bytes)

        return result
