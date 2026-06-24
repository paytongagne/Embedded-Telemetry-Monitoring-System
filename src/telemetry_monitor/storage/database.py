from pathlib import Path
import sqlite3

from telemetry_monitor.core.config import get_settings

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def connect(database_path: str | Path | None = None) -> sqlite3.Connection:
    settings = get_settings()
    target = Path(database_path) if database_path else settings.database_path
    target.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(target, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 5000")
    if settings.enable_sqlite_wal:
        connection.execute("PRAGMA journal_mode = WAL")
    return connection


def initialize_database(connection: sqlite3.Connection) -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    connection.executescript(schema)
    connection.commit()
