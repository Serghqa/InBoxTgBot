from aiogram.fsm.state import State, StatesGroup


class DelMail(StatesGroup):

    main = State()
    deletion = State()
    deleted = State()
