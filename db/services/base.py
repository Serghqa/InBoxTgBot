from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession


class DAO:

    def __init__(
        self,
        dialog_manager: DialogManager,
    ):

        self.session: AsyncSession = \
            dialog_manager.middleware_data.get("db_session")
        self.user_id: int = dialog_manager.event.from_user.id
