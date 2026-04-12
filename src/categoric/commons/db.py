"""Database utilities and helpers."""

import sqlite3
from pathlib import Path
from typing import Any

from loguru import logger


class DatabaseConnection:
    """Context manager for database connections."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn: sqlite3.Connection | None = None

    def __enter__(self) -> sqlite3.Connection:
        """Open database connection."""
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()


def ensure_db_exists(db_path: str) -> None:
    """Ensure database file exists."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()


def execute_db_init(db_path: str, init_sql: str) -> None:
    """Execute initialization SQL on database."""
    ensure_db_exists(db_path)
    with DatabaseConnection(db_path) as conn:
        try:
            with conn:
                conn.executescript(init_sql)
            logger.info(f"Database initialized: {db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database initialization failed: {e}")
            raise


def execute_query(
    db_path: str,
    query: str,
    params: tuple | None = None,
    fetch_one: bool = False,
) -> Any:
    """Execute a SELECT query and return results."""
    with DatabaseConnection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        if fetch_one:
            return cursor.fetchone()
        return cursor.fetchall()


def execute_update(
    db_path: str,
    query: str,
    params: tuple | None = None,
    commit: bool = True,
) -> int:
    """Execute an UPDATE/INSERT/DELETE query and return affected rows."""
    with DatabaseConnection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        if commit:
            conn.commit()
        return cursor.rowcount


def batch_execute(
    db_path: str,
    queries: list[str],
    params_list: list[tuple] | None = None,
) -> None:
    """Execute multiple queries in a transaction."""
    params_list = params_list or [() for _ in queries]
    with DatabaseConnection(db_path) as conn:
        try:
            with conn:
                for query, params in zip(queries, params_list):
                    conn.execute(query, params)
        except sqlite3.Error as e:
            logger.error(f"Batch execute failed: {e}")
            raise
