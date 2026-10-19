"""Представления для работы с типами настроения (moods)."""
import sqlite3
from django.shortcuts import render
from db.database import DB_PATH


def moods(request):
    """Отображает список типов настроения из базы данных SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    moods_list = conn.execute(
        """
        SELECT
            id,
            name,
            description
        FROM moods
        ORDER BY name;
        """
    ).fetchall()
    conn.close()
    return render(request, "moods/mood_list.html", {"moods": moods_list})


def mood_detail(request, mood_id):
    """Отображает информацию о настроении и связанные записи из SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    mood = conn.execute(
        """
        SELECT
            id,
            name,
            description
        FROM moods
        WHERE id = ?;
        """,
        (mood_id,),
    ).fetchone()

    related = []
    if mood is not None:
        related = conn.execute(
            """
            SELECT
                entries.id,
                entries.entry_date,
                entries.score,
                entries.comment,
                users.name AS user_name,
                CASE
                    WHEN entries.score >= 7 THEN 'Хороший день'
                    WHEN entries.score >= 4 THEN 'Нейтральный день'
                    ELSE 'Плохой день'
                END AS status
            FROM entries
            JOIN users ON entries.user_id = users.id
            WHERE entries.mood_id = ?
            ORDER BY entries.entry_date DESC;
            """,
            (mood_id,),
        ).fetchall()

    conn.close()
    return render(
        request,
        "moods/mood_detail.html",
        {"mood": mood, "related_entries": related},
        status=404 if mood is None else 200,
    )
