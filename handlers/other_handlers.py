from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU

last_router: Router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@last_router.message()
async def send_answer(message: Message):
    await message.answer(text=LEXICON_RU['other_answer'])