import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import Config, load_config
from handlers import other_handlers, user_handlers


async def main() -> None:

    config: Config = load_config('settings.ini')

    logging.basicConfig(level=logging.INFO,
                        filename=config.PATH_LOGS, 
                        encoding='utf-8',
                        format='%(asctime)s %(message)s')
    
    storage: MemoryStorage = MemoryStorage()
    
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(storage=storage)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())