"""Модуль подключения к базе данных SQLite."""
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = str(BASE_DIR / "data" / "moodtracker.sqlite")


def get_connection():
    """Создает соединение с базой данных SQLite и включает внешние ключи."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
