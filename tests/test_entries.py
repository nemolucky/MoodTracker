"""Тесты для класса MoodEntry и функций модуля models/entries.py."""
from datetime import date

from models import User
from models.entries import (
    MoodEntry,
    add_mood_entry,
    filter_entries_by_score,
    find_entries_by_date,
    get_average_mood,
    sort_entries_by_score,
)


def make_user() -> User:
    return User(1, "Denis", "denis@example.com")


def test_entry_creation():
    user = make_user()
    entry = MoodEntry(1, date(2026, 9, 13), 8, "Отлично", user)
    assert entry.id == 1
    assert entry.score == 8
    assert entry.comment == "Отлично"
    assert entry.user is user


def test_entry_get_status_good():
    user = make_user()
    entry = MoodEntry(1, date(2026, 9, 13), 8, "", user)
    assert entry.get_status() == "Хороший день"


def test_entry_get_status_neutral():
    user = make_user()
    entry = MoodEntry(1, date(2026, 9, 13), 5, "", user)
    assert entry.get_status() == "Нейтральный день"


def test_entry_get_status_bad():
    user = make_user()
    entry = MoodEntry(1, date(2026, 9, 13), 2, "", user)
    assert entry.get_status() == "Плохой день"


def test_entry_str_contains_user_name():
    user = make_user()
    entry = MoodEntry(1, date(2026, 9, 13), 8, "", user)
    assert "Denis" in str(entry)


def test_validate_score():
    assert MoodEntry.validate_score(5)
    assert MoodEntry.validate_score(0)
    assert MoodEntry.validate_score(10)
    assert not MoodEntry.validate_score(15)
    assert not MoodEntry.validate_score(-1)


def test_add_mood_entry():
    user = make_user()
    entries = []
    add_mood_entry(entries, 1, date(2026, 9, 13), 8, "Отлично", user)
    assert len(entries) == 1
    assert entries[0].user is user


def test_get_average_mood_empty():
    assert get_average_mood([]) == 0.0


def test_get_average_mood():
    user = make_user()
    entries = [
        MoodEntry(1, date(2026, 9, 13), 8, "", user),
        MoodEntry(2, date(2026, 9, 14), 4, "", user),
    ]
    assert get_average_mood(entries) == 6.0


def test_find_entries_by_date():
    user = make_user()
    entries = [
        MoodEntry(1, date(2026, 9, 13), 8, "a", user),
        MoodEntry(2, date(2026, 9, 14), 5, "b", user),
    ]
    found = find_entries_by_date(entries, date(2026, 9, 13))
    assert len(found) == 1
    assert found[0].comment == "a"


def test_filter_entries_by_score():
    user = make_user()
    entries = [
        MoodEntry(1, date(2026, 9, 13), 8, "a", user),
        MoodEntry(2, date(2026, 9, 14), 3, "b", user),
    ]
    filtered = filter_entries_by_score(entries, 5)
    assert len(filtered) == 1
    assert filtered[0].score == 8


def test_sort_entries_by_score():
    user = make_user()
    entries = [
        MoodEntry(1, date(2026, 9, 13), 3, "a", user),
        MoodEntry(2, date(2026, 9, 14), 8, "b", user),
    ]
    sorted_entries = sort_entries_by_score(entries)
    assert sorted_entries[0].score == 3
    assert sorted_entries[1].score == 8