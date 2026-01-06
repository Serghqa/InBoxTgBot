from sqlalchemy.ext.asyncio import AsyncSession


class DAO:

    def __init__(self, session: AsyncSession, user_id: int):

        self.session = session
        self.user_id = user_id
