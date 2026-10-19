"""Скрипт импорта данных из JSON-файлов в базу данных SQLite."""
import json
from db.database import BASE_DIR, get_connection

USERS_FILE = BASE_DIR / "data" / "users.json"
MOODS_FILE = BASE_DIR / "data" / "moods.json"
FACTORS_FILE = BASE_DIR / "data" / "factors.json"
ENTRIES_FILE = BASE_DIR / "data" / "entries.json"


def load_json(filepath):
    """Загружает данные из JSON-файла с кодировкой UTF-8."""
    with open(filepath, encoding="utf-8") as file:
        return json.load(file)


def import_users(conn):
    """Импортирует пользователей в таблицу users."""
    users = load_json(USERS_FILE)
    conn.executemany(
        """
        INSERT INTO users (id, name, email)
        VALUES (?, ?, ?)
        """,
        [(u["id"], u["name"], u.get("email", "")) for u in users],
    )


def import_moods(conn):
    """Импортирует типы настроения в таблицу moods."""
    moods = load_json(MOODS_FILE)
    conn.executemany(
        """
        INSERT INTO moods (id, name, description)
        VALUES (?, ?, ?)
        """,
        [(m["id"], m["name"], m.get("description", "")) for m in moods],
    )


def import_factors(conn):
    """Импортирует факторы влияния в таблицу factors."""
    factors = load_json(FACTORS_FILE)
    conn.executemany(
        """
        INSERT INTO factors (id, name, category)
        VALUES (?, ?, ?)
        """,
        [(f["id"], f["name"], f.get("category", "Общее")) for f in factors],
    )


def import_entries(conn):
    """Импортирует записи настроения и связи с факторами."""
    entries = load_json(ENTRIES_FILE)
    entry_rows = []
    entry_factor_rows = []

    for entry in entries:
        entry_rows.append(
            (
                entry["id"],
                entry["user_id"],
                entry.get("mood_id"),
                entry["entry_date"],
                entry["score"],
                entry.get("comment", ""),
            )
        )
        for factor_id in entry.get("factor_ids", []):
            entry_factor_rows.append((entry["id"], factor_id))

    conn.executemany(
        """
        INSERT INTO entries (
            id, user_id, mood_id, entry_date, score, comment
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        entry_rows,
    )
    if entry_factor_rows:
        conn.executemany(
            """
            INSERT INTO entry_factors (entry_id, factor_id)
            VALUES (?, ?)
            """,
            entry_factor_rows,
        )


def main():
    """Точка входа скрипта импорта."""
    conn = get_connection()
    try:
        import_users(conn)
        import_moods(conn)
        import_factors(conn)
        import_entries(conn)
        conn.commit()
        print("Импорт данных из JSON в SQLite успешно завершен.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
