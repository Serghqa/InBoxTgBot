from aiogram.fsm.state import State, StatesGroup


class Mail(StatesGroup):

    main = State()
    calendar = State()
