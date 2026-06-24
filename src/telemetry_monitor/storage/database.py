from pathlib import Path
import sqlite3

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def connect(database_path: str = "telemetry.db") -> sqlite3.Connection:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(connection: sqlite3.Connection) -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    connection.executescript(schema)
    connection.commit()
