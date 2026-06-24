from pathlib import Path
import sqlite3

SCHEMA_PATH = Path(__file__).with_name("schema.sql")
DEFAULT_DATABASE_PATH = Path("data/telemetry.db")


def connect(database_path: str | None = None) -> sqlite3.Connection:
    target = Path(database_path) if database_path else DEFAULT_DATABASE_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(target)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(connection: sqlite3.Connection) -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    connection.executescript(schema)
    connection.commit()
