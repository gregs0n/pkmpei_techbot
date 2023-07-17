from aiogram.filters.state import State, StatesGroup


class FSMAddTicket(StatesGroup):
    fill_ticket = State()