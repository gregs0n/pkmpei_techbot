from sqlite3 import connect

def main() -> None:
    with connect("database.db") as conn:
        conn.execute(_c_status_query)
        conn.execute('INSERT INTO c_status(statusName) VALUES ("В работе"), ("Завершен");')
        conn.execute(_users_query)
        conn.execute(_tickets_query)
        

_c_status_query = """
CREATE TABLE IF NOT EXISTS c_status(
    idStatus INTEGER PRIMARY KEY,
    statusName TEXT NOT NULL,
    FOREIGN KEY (idStatus)
        REFERENCES tickets (idStatus)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);
"""

_users_query = """
CREATE TABLE IF NOT EXISTS users(
    idUser INTEGER PRIMARY KEY,
    userName TEXT NOT NULL,
    FOREIGN KEY (idUser)
        REFERENCES tickets (idUser)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);
"""

_tickets_query = """
CREATE TABLE IF NOT EXISTS tickets(
    id INTEGER PRIMARY KEY,
    idUser INTEGER NOT NULL,
    text TEXT NOT NULL,
    idStatus INTEGER DEFAULT 1,
    ts TIMESTAMP
);
"""

if __name__ == "__main__":
    main()