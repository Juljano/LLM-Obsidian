import os
import sqlite3
import os.path as File


def create_database(db_name):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()


def insert_message(db_name, conversation_id, role, content):

    if not os.path.exists(db_name):
        create_database(db_name)

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO conversation
            (conversation_id, role, content)
            VALUES (?, ?, ?)
        """,
            (conversation_id, role, content),
        )


def read_history_messages(db_name) -> list:

    if not os.path.exists(db_name):
        create_database(db_name)

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT role, content
                FROM conversation
                ORDER BY id ASC
            """)

            rows = cursor.fetchall()

            return [{"role": role, "content": content} for role, content in rows]

    except sqlite3.Error as e:
        print(f"Fehler beim Lesen der Tabelle: {e}")

        return []


def insert_memory(db_name: str, content: str) -> None:
    if not os.path.exists(db_name):
        create_database(db_name)

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                           INSERT INTO memory
                               (content)
                           VALUES (?)
                           """,
                (content,),
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
                           SELECT id, content, created_at
                           FROM memory
                           ORDER BY id ASC
                           """)

            rows = cursor.fetchall()

            return [
                {"id": id, "content": content, "created_at": created_at}
                for id, content, created_at in rows
            ]

    except sqlite3.Error as e:
        print(f"Fehler beim Lesen der Memory-Tabelle: {e}")
        return []
