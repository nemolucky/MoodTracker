"""Представления для работы с записями настроения (entries)."""
import sqlite3
from django.shortcuts import render
from db.database import DB_PATH


def entries(request):
    """Отображает список записей настроения из базы данных SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    entries_list = conn.execute(
        """
        SELECT
            entries.id,
            entries.entry_date,
            entries.score,
            entries.comment,
            users.name AS user_name,
            moods.name AS mood_name,
            CASE
                WHEN entries.score >= 7 THEN 'Хороший день'
                WHEN entries.score >= 4 THEN 'Нейтральный день'
                ELSE 'Плохой день'
            END AS status
        FROM entries
        JOIN users ON entries.user_id = users.id
        LEFT JOIN moods ON entries.mood_id = moods.id
        ORDER BY entries.entry_date DESC;
        """
    ).fetchall()
    conn.close()
    return render(
        request, "entries/entry_list.html", {"entries": entries_list}
    )


def entry_detail(request, entry_id):
    """Отображает детальную информацию о записи настроения из SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    entry = conn.execute(
        """
        SELECT
            entries.id,
            entries.entry_date,
            entries.score,
            entries.comment,
            users.name AS user_name,
            users.email AS user_email,
            moods.id AS mood_id,
            moods.name AS mood_name,
            CASE
                WHEN entries.score >= 7 THEN 'Хороший день'
                WHEN entries.score >= 4 THEN 'Нейтральный день'
                ELSE 'Плохой день'
            END AS status
        FROM entries
        JOIN users ON entries.user_id = users.id
        LEFT JOIN moods ON entries.mood_id = moods.id
        WHERE entries.id = ?;
        """,
        (entry_id,),
    ).fetchone()

    factors = []
    if entry is not None:
        factors = conn.execute(
            """
            SELECT factors.id, factors.name, factors.category
            FROM factors
            JOIN entry_factors ON factors.id = entry_factors.factor_id
            WHERE entry_factors.entry_id = ?
            ORDER BY factors.name;
            """,
            (entry_id,),
        ).fetchall()

    conn.close()
    return render(
        request,
        "entries/entry_detail.html",
        {"entry": entry, "factors": factors},
        status=404 if entry is None else 200,
    )


def search_by_date(request):
    """Поиск записей и неиспользованных настроений на выбранную дату."""
    search_date = request.GET.get("date", "").strip()
    found_entries = []
    unused_moods = []

    if search_date:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        found_entries = conn.execute(
            """
            SELECT
                entries.id,
                entries.entry_date,
                entries.score,
                entries.comment,
                users.name AS user_name,
                moods.name AS mood_name,
                CASE
                    WHEN entries.score >= 7 THEN 'Хороший день'
                    WHEN entries.score >= 4 THEN 'Нейтральный день'
                    ELSE 'Плохой день'
                END AS status
            FROM entries
            JOIN users ON entries.user_id = users.id
            LEFT JOIN moods ON entries.mood_id = moods.id
            WHERE entries.entry_date = ?
            ORDER BY entries.id;
            """,
            (search_date,),
        ).fetchall()

        unused_moods = conn.execute(
            """
            SELECT moods.id, moods.name, moods.description
            FROM moods
            WHERE moods.id NOT IN (
                SELECT entries.mood_id
                FROM entries
                WHERE entries.entry_date = ?
                  AND entries.mood_id IS NOT NULL
            )
            ORDER BY moods.name;
            """,
            (search_date,),
        ).fetchall()
        conn.close()

    context = {
        "search_date": search_date,
        "entries": found_entries,
        "unused_moods": unused_moods,
    }
    return render(request, "entries/search.html", context)


def statistics(request):
    """Отображает аналитическую статистику по записям и настроениям."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    mood_stats = conn.execute(
        """
        SELECT
            moods.id AS mood_id,
            moods.name AS mood_name,
            COUNT(entries.id) AS entries_count,
            ROUND(AVG(entries.score), 1) AS avg_score
        FROM moods
        LEFT JOIN entries ON moods.id = entries.mood_id
        GROUP BY moods.id, moods.name
        ORDER BY entries_count DESC, moods.name ASC;
        """
    ).fetchall()

    overall = conn.execute(
        """
        SELECT
            COUNT(*) AS total_entries,
            ROUND(AVG(score), 1) AS avg_score,
            MIN(score) AS min_score,
            MAX(score) AS max_score
        FROM entries;
        """
    ).fetchone()

    category_stats = conn.execute(
        """
        SELECT
            category,
            COUNT(*) AS factors_count
        FROM factors
        GROUP BY category
        ORDER BY factors_count DESC, category ASC;
        """
    ).fetchall()

    conn.close()
    context = {
        "mood_stats": mood_stats,
        "overall": overall,
        "category_stats": category_stats,
    }
    return render(request, "entries/statistics.html", context)
