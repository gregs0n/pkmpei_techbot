from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_inline_kb(width: int,
                     **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()

state_keyboard: dict[str, str] = {
    'query_type' : 'Написать/изменить запрос📑',
    'network_type' : 'Починить интернет📶',
    'printer_type' : 'Не работает принтер/сканер🖨',
    'email_type' : 'Отправить email-рассылку📧',
    'other_type' : 'Прочее💣',
}