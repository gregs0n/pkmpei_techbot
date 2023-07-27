from aiogram import Router
from aiogram.filters import Command, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon import LEXICON_RU
from states.states import FSMUserStatus
from services.user_methods import *
from services.admin_methods import *
from exceptions.exceptions import BotException
from filters.filters import IsAdmin
from keyboards.keyboards import create_inline_kb

admin_router: Router = Router()
admin_router.message.filter(StateFilter(FSMUserStatus.admin))
## admin_router.message.filter(IsAdmin())


@admin_router.message(Command(commands='user'))
async def process_user(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer("Теперь вы юзер!")

@admin_router.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(text=LEXICON_RU['admin_help'])

@admin_router.message(Command(commands='list_tickets'))
async def process_show_all(message: Message):
    sent_tickets = ListTickets()
    await message.answer(text=LEXICON_RU['/list_tickets'])
    kb = create_inline_kb(2,
                          cb_close_ticket="Закрыть",
                          cb_remove_ticket="Удалить")
    for ticket in sent_tickets:
        await message.answer(text=ticket,
                             reply_markup=kb)

@admin_router.message(Command(commands='close_ticket'))
async def process_close_ticket(message: Message):
    try:
        idTicket: int = int(message.text.split()[1])
        await message.answer(CloseTicket(idTicket))
    except BotException as exc:
        await message.answer(text=str(exc))

@admin_router.message(Command(commands='remove_ticket'))
async def process_remove_ticket(message: Message):
    try:
        idTicket: int = int(message.text.split()[1])
        await message.answer(RemoveTicket(idTicket))
    except TicketNotFoundException as exc:
        await message.answer(text=str(exc))

@admin_router.callback_query(Text(text=['cb_remove_ticket']))
async def process_remove_ticket(callback: CallbackQuery):
    try:
        idTicket: int = int(callback.message.text.split()[0][7:])
        await callback.answer(RemoveTicket(idTicket))
    except TicketNotFoundException as exc:
        await callback.answer(text=str(exc))

@admin_router.callback_query(Text(text=['cb_close_ticket']))
async def process_close_ticket(callback: CallbackQuery):
    try:
        print(callback.message.text)
        print(callback.message.text.split())
        print(callback.message.text.split()[1])
        idTicket: int = int(callback.message.text.split()[0][7:])
        await callback.answer(CloseTicket(idTicket))
    except BotException as exc:
        await callback.answer(text=str(exc))