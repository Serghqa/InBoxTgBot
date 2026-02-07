from aiogram.fsm.state import State, StatesGroup


class SelectLetter(StatesGroup):

    main = State()
    letter = State()
    text = State()
    attachment = State()
