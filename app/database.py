"""Persistência SQLite com uma conexão curta por operação."""

import sqlite3
from contextlib import closing
from pathlib import Path


class TaskStore:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=5)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection, connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL CHECK(length(trim(title)) BETWEEN 1 AND 200),
                    status TEXT NOT NULL DEFAULT 'pending'
                        CHECK(status IN ('pending', 'completed'))
                )
                """
            )

    def create(self, title: str) -> dict:
        with closing(self._connect()) as connection, connection:
            cursor = connection.execute("INSERT INTO tasks(title) VALUES (?)", (title,))
            row = connection.execute(
                "SELECT id, title, status FROM tasks WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
            return dict(row)

    def list_all(self) -> list[dict]:
        with closing(self._connect()) as connection:
            rows = connection.execute(
                "SELECT id, title, status FROM tasks ORDER BY id"
            ).fetchall()
            return [dict(row) for row in rows]

    def complete(self, task_id: int) -> dict | None:
        with closing(self._connect()) as connection, connection:
            cursor = connection.execute(
                "UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,)
            )
            if cursor.rowcount == 0:
                return None
            row = connection.execute(
                "SELECT id, title, status FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
            return dict(row)

    def check_health(self) -> None:
        # A consulta verifica conexão e tabela; não basta o processo estar ativo.
        with closing(self._connect()) as connection:
            connection.execute("SELECT id FROM tasks LIMIT 1").fetchall()
