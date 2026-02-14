from aiogram.fsm.state import State, StatesGroup


class AddMail(StatesGroup):

    main = State()
    login = State()
    password = State()
    add_mail = State()
    success_mail = State()
