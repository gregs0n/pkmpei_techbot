from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from states.states import FSMAddTicket, FSMUserStatus
from services.user_methods import AddTicket, ListTickets
from config.config import load_config
from exceptions.exceptions import BotException

user_router: Router = Router()
user_router.message.filter(~StateFilter(FSMUserStatus.admin))


@user_router.message(CommandStart())
async def process_start(message: Message):
    await message.answer(text=LEXICON_RU['/start'])

@user_router.message(Command(commands='admin'))
async def process_admin(message: Message, state: FSMContext):
    if (message.from_user.id in load_config('settings.ini').ADMINS):
        await state.set_state(FSMUserStatus.admin)
        await message.answer("Теперь вы админ!")
    else:
        await message.answer("Вас нет в списке админов!")

@user_router.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(text=LEXICON_RU['user_help'])

@user_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/cancel'])
    await state.clear()

@user_router.message(Command(commands='add_ticket'), StateFilter(default_state))
async def process_start_input(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/add_ticket'])
    await state.set_state(FSMAddTicket.fill_ticket)

@user_router.message(StateFilter(FSMAddTicket.fill_ticket))
async def process_finish_input(message: Message, state: FSMContext):
    try:
        ticket_id: int = AddTicket(message.from_user.id,
                                   message.from_user.username,
                                   message.text)
        await message.answer(text=LEXICON_RU['new_ticket_msg'].format(ticket_id))
        await state.clear()
    except BotException as exc:
        await message.answer(text=str(exc))
    
@user_router.message(Command(commands='list_tickets'), StateFilter(default_state))
async def process_show_sent(message: Message):
    sent_tickets = ListTickets(message.from_user.id)
    await message.answer(text=LEXICON_RU['/list_tickets'] + '\n\n'.join(sent_tickets))
