"""Тесты для базы данных SQLite, схемы и SQL-запросов (ПР7)."""
from pathlib import Path
import sqlite3

from db.database import DB_PATH, get_connection


def test_get_connection():
    """Соединение с БД устанавливается и PRAGMA foreign_keys включена."""
    conn = get_connection()
    assert conn is not None
    fk_status = conn.execute("PRAGMA foreign_keys").fetchone()[0]
    assert fk_status == 1
    conn.close()


def test_required_tables_exist():
    """Все необходимые таблицы предметной области созданы в SQLite."""
    conn = get_connection()
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    tables = {row[0] for row in cursor.fetchall()}
    conn.close()

    expected_tables = {
        "users",
        "moods",
        "factors",
        "entries",
        "entry_factors",
    }
    assert expected_tables.issubset(tables)


def test_database_has_records():
    """Таблицы базы данных содержат импортированные данные."""
    conn = get_connection()
    users_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    moods_count = conn.execute("SELECT COUNT(*) FROM moods").fetchone()[0]
    factors_count = conn.execute("SELECT COUNT(*) FROM factors").fetchone()[0]
    entries_count = conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
    entry_factors_count = conn.execute(
        "SELECT COUNT(*) FROM entry_factors"
    ).fetchone()[0]
    conn.close()

    assert users_count >= 1
    assert moods_count >= 4
    assert factors_count >= 5
    assert entries_count >= 4
    assert entry_factors_count >= 2


def test_queries_file_executes_successfully():
    """Все запросы из файла sql/queries.sql корректно выполняются."""
    queries_file = Path(DB_PATH).parent.parent / "sql" / "queries.sql"
    assert queries_file.exists()

    with open(queries_file, encoding="utf-8") as file:
        content = file.read()

    statements = [s.strip() for s in content.split(";") if s.strip()]
    assert len(statements) >= 10

    conn = sqlite3.connect(DB_PATH)
    for stmt in statements:
        sql_lines = [
            line for line in stmt.splitlines()
            if not line.strip().startswith("--")
        ]
        query = "\n".join(sql_lines).strip()
        if not query:
            continue
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        assert rows is not None
    conn.close()
