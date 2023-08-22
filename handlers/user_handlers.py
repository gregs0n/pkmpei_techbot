from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON_RU, ticket_type_keyboard, ticket_recommendations
from states.states import FSMAddTicket, FSMUserStatus
from services.user_methods import AddTicket, ListTickets
from config.config import load_config
from exceptions.exceptions import BotException
from keyboards.keyboards import create_inline_kb

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

@user_router.message(Command(commands='add_ticket'), StateFilter(default_state))
async def process_start_input(message: Message, state: FSMContext):
    sent_msg = await message.answer(
        text=LEXICON_RU['select_category'],
        reply_markup=create_inline_kb(width=1, **ticket_type_keyboard)
        )
    await state.set_state(FSMAddTicket.fill_type)
    await state.update_data(sent_message=sent_msg)

@user_router.callback_query(Text("cancel"))
async def process_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=LEXICON_RU['/cancel'])
    state_data = await state.get_data()
    await state_data['sent_message'].delete()
    await state.clear()

@user_router.callback_query(Text(endswith="_type"), StateFilter(FSMAddTicket.fill_type))
async def process_ticket_type_select(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON_RU['/add_ticket'].format(
            ticket_type_keyboard[callback.data],
            ticket_recommendations[callback.data]),
        reply_markup=create_inline_kb(
            width=1,
            cancel=ticket_type_keyboard["cancel"])
        )
    _id_category = list(ticket_type_keyboard.keys()).index(callback.data)+1
    await state.update_data(idCategory=_id_category)
    await state.set_state(FSMAddTicket.fill_ticket)

@user_router.message(StateFilter(FSMAddTicket.fill_ticket))
async def process_finish_input(message: Message, state: FSMContext):
    try:
        state_data = await state.get_data()
        ticket_id: int = AddTicket(message.from_user.id,
                                   message.from_user.username,
                                   message.text,
                                   state_data['idCategory'])
        await message.answer(text=LEXICON_RU['new_ticket_msg'].format(ticket_id))
        await state.clear()
    except BotException as exc:
        await message.answer(text=str(exc))
    
@user_router.message(Command(commands='list_tickets'), StateFilter(default_state))
async def process_show_sent(message: Message):
    sent_tickets = ListTickets(message.from_user.id)
    await message.answer(text=LEXICON_RU['/list_tickets'] + '\n\n'.join(sent_tickets))
