from aiogram.fsm.state import State, StatesGroup

class FSMUserStatus(StatesGroup):
    admin = State()
    user = State()

class FSMAddTicket(StatesGroup):
    fill_ticket = State()
    query_type = State()
    network_type = State()
    printer_type = State()
    email_type = State()
    other_type = State()