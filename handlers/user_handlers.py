from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from states.states import FSMAddTicket
from services.services import AddTicket, ListTickets

router: Router = Router()


@router.message(CommandStart())
async def process_start(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(text=LEXICON_RU['/help'])

@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/cancel'])
    await state.clear()

@router.message(Command(commands='add_ticket'), StateFilter(default_state))
async def process_start_input(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/add_ticket'])
    await state.set_state(FSMAddTicket.fill_ticket)

@router.message(StateFilter(FSMAddTicket.fill_ticket))
async def process_finish_input(message: Message, state: FSMContext):
    ticket_id: int = AddTicket(message.from_user.id,
                               message.from_user.username,
                               message.text)
    await message.answer(text=LEXICON_RU['new_ticket'].format(ticket_id))
    await state.clear()
    
@router.message(Command(commands='watch_sent'), StateFilter(default_state))
async def process_show_sent(message: Message):
    await message.answer(text=LEXICON_RU['/watch_tickets'] + ListTickets(message.from_user.id))

@router.message(Command(commands='watch_all'), StateFilter(default_state))
async def process_show_all(message: Message):
    await message.answer(text=LEXICON_RU['/watch_tickets'] + ListTickets(message.from_user.id))