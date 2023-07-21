from sqlite3 import connect
from datetime import datetime
from config.config import load_config
from exceptions.exceptions import *

def AddTicket(iduser: int,
              userName: str,
              text: str) -> int:
    ticket_id: int = 0
    config = load_config('settings.ini')
    with connect(config.PATH_DATABASE) as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tickets WHERE idUser=? AND idStatus=1", (iduser,))
        tickets = cursor.fetchall()
        if len(tickets) >= 3:
            raise TicketLimitException("Превышено количество необработанных исходящих тикетов!")
        
        cursor.execute("SELECT * FROM users WHERE idUser=?", (iduser,))
        if (cursor.fetchone() is None):
            cursor.execute("INSERT INTO users(idUser,userName) VALUES(?,?)",
                           (iduser, userName))
        
        cursor.execute("INSERT INTO tickets(idUser,text,ts) VALUES(?,?,?)",
                       (iduser, text, datetime.now()))
        ticket_id = cursor.lastrowid
    return ticket_id

def ListTickets(iduser: int = 0) -> str:
    query: str = """
                SELECT
                    id,
                    userName,
                    text,
                    statusName
                FROM
                    tickets
                    INNER JOIN users USING (idUser)
                    INNER JOIN c_status USING (idStatus)
                """
    params = ()
    if iduser != 0:
        query += "WHERE idStatus=1 AND idUser=?"
        params = (iduser,)
    else:
        query += "WHERE idStatus=1"
    config = load_config('settings.ini')
    rows: list[tuple] = []
    result: list[str] = []
    with connect(config.PATH_DATABASE) as conn:
        cursor = conn.cursor()
        rows = cursor.execute(query, params).fetchall()
    for row in rows:
        if iduser == 0:
            max_len = -1
        else:
            max_len = min(len(row[2]), 75)
        ticket_field = row[2][:max_len]
        row_string = f"Ticket#{row[0]} by @{row[1]}:\n\t{ticket_field} - {row[3]}"
        result.append(row_string)
    return result
