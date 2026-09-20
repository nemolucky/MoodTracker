from datetime import date

from entries import (
    add_mood_entry,
    filter_entries_by_score,
    find_entries_by_date,
    get_average_mood,
    get_day_status,
    sort_entries_by_score,
)


def test_add_mood_entry():
    entries = []
    add_mood_entry(entries, date(2026, 9, 13), 8, "Отлично")
    assert len(entries) == 1
    assert entries[0]["score"] == 8


def test_get_day_status_good():
    assert get_day_status(8) == "Хороший день"


def test_get_day_status_neutral():
    assert get_day_status(5) == "Нейтральный день"


def test_get_day_status_bad():
    assert get_day_status(2) == "Плохой день"


def test_get_average_mood_empty():
    assert get_average_mood([]) == 0.0


def test_get_average_mood():
    entries = [
        {"entry_date": date(2026, 9, 13), "score": 8, "comment": ""},
        {"entry_date": date(2026, 9, 14), "score": 4, "comment": ""},
    ]
    assert get_average_mood(entries) == 6.0


def test_find_entries_by_date():
    entries = [
        {"entry_date": date(2026, 9, 13), "score": 8, "comment": "a"},
        {"entry_date": date(2026, 9, 14), "score": 5, "comment": "b"},
    ]
    found = find_entries_by_date(entries, date(2026, 9, 13))
    assert len(found) == 1
    assert found[0]["comment"] == "a"


def test_filter_entries_by_score():
    entries = [
        {"entry_date": date(2026, 9, 13), "score": 8, "comment": "a"},
        {"entry_date": date(2026, 9, 14), "score": 3, "comment": "b"},
    ]
    filtered = filter_entries_by_score(entries, 5)
    assert len(filtered) == 1
    assert filtered[0]["score"] == 8


def test_sort_entries_by_score():
    entries = [
        {"entry_date": date(2026, 9, 13), "score": 3, "comment": "a"},
        {"entry_date": date(2026, 9, 14), "score": 8, "comment": "b"},
    ]
    sorted_entries = sort_entries_by_score(entries)
    assert sorted_entries[0]["score"] == 3
    assert sorted_entries[1]["score"] == 8