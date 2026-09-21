from datetime import date
from typing import List, Optional

from .users import User


class MoodEntry:

    def __init__(
        self,
        entry_id: int,
        entry_date: date,
        score: int,
        comment: str,
        user: User,
    ) -> None:
        self.id = entry_id
        self.entry_date = entry_date
        self.score = score
        self.comment = comment
        self.user = user

    def get_status(self) -> str:
        if self.score >= 7:
            return "Хороший день"
        elif self.score >= 4:
            return "Нейтральный день"
        return "Плохой день"

    def __str__(self) -> str:
        return (
            f"{self.entry_date} | {self.user.name} | "
            f"{self.score}/10 | {self.get_status()}"
        )

    @staticmethod
    def validate_score(score: int) -> bool:
        return 0 <= score <= 10


def add_mood_entry(
    entries: List[MoodEntry],
    entry_id: int,
    entry_date: date,
    score: int,
    comment: str,
    user: User,
) -> MoodEntry:
    new_entry = MoodEntry(entry_id, entry_date, score, comment, user)
    entries.append(new_entry)
    return new_entry


def find_entry_by_id(
    entries: List[MoodEntry],
    entry_id: int,
) -> Optional[MoodEntry]:
    for entry in entries:
        if entry.id == entry_id:
            return entry
    return None


def find_entries_by_date(
    entries: List[MoodEntry],
    target_date: date,
) -> List[MoodEntry]:
    return [entry for entry in entries if entry.entry_date == target_date]


def filter_entries_by_score(
    entries: List[MoodEntry],
    min_score: int,
) -> List[MoodEntry]:
    return [entry for entry in entries if entry.score >= min_score]


def sort_entries_by_score(
    entries: List[MoodEntry],
    reverse: bool = False,
) -> List[MoodEntry]:
    return sorted(
        entries,
        key=lambda entry: entry.score,
        reverse=reverse,
    )


def get_average_mood(entries: List[MoodEntry]) -> float:
    if not entries:
        return 0.0
    total = sum(entry.score for entry in entries)
    return round(total / len(entries), 1)


def get_mood_trend(entries: List[MoodEntry], last_n: int = 3) -> str:
    if len(entries) < last_n * 2:
        return "Недостаточно данных для оценки тенденции"

    sorted_by_date = sorted(entries, key=lambda entry: entry.entry_date)
    recent = sorted_by_date[-last_n:]
    previous = sorted_by_date[-last_n * 2:-last_n]

    recent_avg = get_average_mood(recent)
    previous_avg = get_average_mood(previous)

    if recent_avg > previous_avg:
        return "Настроение улучшается"
    elif recent_avg < previous_avg:
        return "Настроение ухудшается"
    return "Настроение стабильно"
