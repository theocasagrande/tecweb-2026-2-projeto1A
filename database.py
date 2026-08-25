import sqlite3
from dataclasses import dataclass


@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''


class Database:
    def __init__(self, name):
        self.conn = sqlite3.connect(f'{name}.db')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS note (
                id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT NOT NULL
            )
        ''')

    def add(self, note):
        self.conn.execute(
            'INSERT INTO note (title, content) VALUES (?, ?)',
            (note.title, note.content)
        )
        self.conn.commit()
