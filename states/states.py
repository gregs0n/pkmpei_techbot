from aiogram.fsm.state import State, StatesGroup

class FSMUserStatus(StatesGroup):
    admin = State()
    user = State()

class FSMAddTicket(StatesGroup):
    fill_ticket = State()
    fill_type = State()
