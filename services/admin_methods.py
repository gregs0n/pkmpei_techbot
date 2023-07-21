from sqlite3 import connect
from config.config import load_config
from exceptions.exceptions import *

def CloseTicket(idTicket: int) -> str:
    config = load_config('settings.ini')
    with connect(config.PATH_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT idStatus FROM tickets WHERE id=?",
            (idTicket,)
            )
        ticket_status = cursor.fetchone()
        if ticket_status is None:
            raise TicketNotFoundException(f"Тикет #{idTicket} не найден")
        elif ticket_status == 2:
            raise TicketClosedException(f"Тикет #{idTicket} уже закрыт")
        cursor.execute(
            "UPDATE tickets SET idStatus=2 WHERE id=?",
            (idTicket,)
        )
    return f"Тикет #{idTicket} успешно закрыт"

def RemoveTicket(idTicket: int):
    config = load_config('settings.ini')
    with connect(config.PATH_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tickets WHERE id=?",
            (idTicket,)
            )
        if cursor.fetchone() is None:
            raise TicketNotFoundException(f"Тикет #{idTicket} не найден")
        cursor.execute(
            "DELETE FROM tickets WHERE id=?",
            (idTicket,)
        )
    return f"Тикет #{idTicket} успешно удален"