import os
import sqlite3


def create_database(db_name):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

def insert_memory(db_name, role, content) -> None:
    if not os.path.exists(db_name):
        create_database(db_name)

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                           INSERT INTO memory
                               (role, content)
                           VALUES (?, ?)
                           """,
                (role, content),
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"Fehler beim Einfügen des Speichereintrags: {e}")


def read_memory(db_name: str):

    if not os.path.exists(db_name):
        create_database(db_name)

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT role, content
                           FROM memory
                           ORDER BY id ASC
                           """)

            rows = cursor.fetchall()

        return [{"role": role, "content": content} for role, content in rows]

    except sqlite3.Error as e:
        print(f"Fehler beim Lesen der Memory-Tabelle: {e}")
        return []
    
    
