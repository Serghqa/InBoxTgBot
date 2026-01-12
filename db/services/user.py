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

    async def del_imap_credentials(
        self,
        email: str,
        imap_server: str
    ) -> ImapCredentials | None:

        imap_credentials: ImapCredentials | None = \
            await self.get_imap_credentials(
                email=email,
                imap_server=imap_server
            )

        if imap_credentials is not None:
            await self.session.delete(imap_credentials)
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
