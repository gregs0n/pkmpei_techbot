LEXICON_RU: dict[str, str] = {
'/start':
"""
Привет!
Я бот внутренней техподдержки ПК МЭИ.

Оставить заявку можно командой /add_ticket
Или можете отправить команду /help, чтобы
посмотреть список всех доступных Вам команд.
""",

'user_help':
"""
Список доступных команд:

/add_ticket - Добавить новую заявку
/watch_sent - Посмотреть исходящие заявки
""",

'admin_help':
"""
Список доступных команд:

/watch_all - Посмотреть все текущие заявки
/close_ticket N - Отметить заявку N как выполненную
/remove_ticket N - Удалить заявку с номером N
""",

'no_echo':
"""
Данный тип апдейтов не поддерживается
методом send_copy
""",

'/cancel': 'Заявка отменена',
'/add_ticket': 'Введите текст заявки:',
'new_ticket_msg': 'Ваша заявка принята!\nНомер заявки - #{}',
'/watch_tickets': 'Список заявок:\n',
'/close_ticket':
"""
Тикет #{} успешно закрыт.
"""
}

LEXICON_COMMANDS_RU: dict[str, str] = {
    '/start' : 'Начало работы',
    '/help' : 'Справка по работе бота',
    '/add_ticket' : 'Добавить новую заявку',
    '/watch_sent' : 'Посмотреть исходящие заявки',
}