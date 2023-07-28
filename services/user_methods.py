from sqlite3 import connect
from datetime import datetime
from config.config import load_config
from exceptions.exceptions import *

def AddTicket(iduser: int,
              userName: str,
              text: str,
              idCategory: int = 5) -> int:
    ticket_id: int = 0
    config = load_config('settings.ini')
    with connect(config.PATH_DATABASE) as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM tickets WHERE idUser=? AND idStatus<3",
            (iduser,))
        tickets = cursor.fetchall()
        if len(tickets) > config.MAX_TICKETS:
            raise TicketLimitException(
                "Превышено количество необработанных исходящих тикетов!"
                )
        
        cursor.execute(
            "SELECT * FROM users WHERE idUser=?",
            (iduser,))
        if (cursor.fetchone() is None):
            cursor.execute(
                "INSERT INTO users(idUser,userName) VALUES(?,?)",
                (iduser, userName))
        
        cursor.execute(
            "INSERT INTO tickets(idUser,text,idCategory,ts) VALUES(?,?,?,?)",
            (iduser, text, idCategory, datetime.now()))
        ticket_id = cursor.lastrowid
    return ticket_id

def ListTickets(iduser: int = 0) -> str:
    query = GET_TICKET_QUERY
    params = ()
    if iduser != 0:
        query += "WHERE idUser=?"
        params = (iduser,)
    else:
        query += "WHERE idStatus<>3"
    config = load_config('settings.ini')
    rows: list[tuple] = []
    result: list[str] = []
    with connect(config.PATH_DATABASE) as conn:
        cursor = conn.cursor()
        rows = cursor.execute(query, params).fetchall()
    for row in rows:
        row_string = GetTicketString(*row)
        result.append(row_string)
    return result

def GetTicketString(idTicket: int,
                    userName: str,
                    category: str,
                    status: str,
                    text: str) -> str:
    ticket_lines = [f"Ticket#{idTicket} by @{userName}",
                    f"Type: {category}",
                    f"Status: {status}",
                    text]
    return '\n'.join(ticket_lines)

GET_TICKET_QUERY = """
SELECT
    id,
    userName,
    categoryName,
    statusName,
    text
FROM
    tickets
    INNER JOIN users USING (idUser)
    INNER JOIN c_status USING (idStatus)
    INNER JOIN c_category USING (idCategory)
"""