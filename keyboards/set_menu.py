from aiogram import Bot
from aiogram.types import BotCommand

async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/start',
                   description='Начало работы'),
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/add_ticket',
                   description='Добавить новую заявку'),
        BotCommand(command='/watch_sent',
                   description='Посмотреть исходящие заявки')]

    await bot.set_my_commands(main_menu_commands)