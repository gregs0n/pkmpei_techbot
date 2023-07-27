from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon import LEXICON_COMMANDS_RU

async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command=cmd,
                   description=descr)
        for cmd, descr in LEXICON_COMMANDS_RU.items()]

    await bot.set_my_commands(main_menu_commands)