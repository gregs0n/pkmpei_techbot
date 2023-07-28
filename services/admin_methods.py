from sqlite3 import connect
from config.config import load_config
from exceptions.exceptions import *
from .user_methods import GetTicketString, GET_TICKET_QUERY

def UpdateTicketStatus(idTicket: int) -> str:
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
        elif ticket_status[0] == 3:
            raise TicketClosedException(f"Тикет #{idTicket} уже закрыт")
        cursor.execute(
            "UPDATE tickets SET idStatus=? WHERE id=?",
            (ticket_status[0]+1, idTicket)
        )
        cursor.execute(GET_TICKET_QUERY + "WHERE id=?",
                                (idTicket,)
                                )
        ticket = cursor.fetchone()
    return f"Сатус тикета #{idTicket} успешно изменен", GetTicketString(*ticket)

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