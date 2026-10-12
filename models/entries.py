"""Модель для сущности MoodEntry (Запись настроения)."""
from datetime import date
from typing import List, Optional

from .users import User
from .moods import Mood
from .factors import Factor


class MoodEntry:
    """Представляет одну запись о настроении пользователя."""

    def __init__(
        self,
        entry_id: int,
        entry_date: date,
        score: int,
        comment: str,
        user: User,
        mood: Optional[Mood] = None,
        factors: Optional[List[Factor]] = None,
    ) -> None:
        self.id = entry_id
        self.entry_date = entry_date
        self.score = score
        self.comment = comment
        self.user = user
        self.mood = mood
        self.factors = factors if factors is not None else []

    def get_status(self) -> str:
        """Возвращает текстовое описание статуса дня."""
        if self.score >= 7:
            return "Хороший день"
        elif self.score >= 4:
            return "Нейтральный день"
        return "Плохой день"

    def __str__(self) -> str:
        """Строковое представление записи для вывода в консоль."""
        base_str = (
            f"{self.entry_date} | {self.user.name} | "
            f"{self.score}/10 | {self.get_status()}"
        )

        mood_str = ""
        if self.mood:
            mood_str = f" | Настроение: {self.mood.name}"

        factors_str = ""
        if self.factors:
            factor_names = ", ".join([f.name for f in self.factors])
            factors_str = f" | Факторы: {factor_names}"

        return base_str + mood_str + factors_str

    @staticmethod
    def validate_score(score: int) -> bool:
        """Проверяет, находится ли оценка в допустимом диапазоне."""
        return 0 <= score <= 10


def add_mood_entry(
    entries: List[MoodEntry],
    entry_id: int,
    entry_date: date,
    score: int,
    comment: str,
    user: User,
    mood: Optional[Mood] = None,
    factors: Optional[List[Factor]] = None,
) -> MoodEntry:
    """Создает новую запись и добавляет её в список."""
    new_entry = MoodEntry(
        entry_id, entry_date, score, comment, user, mood, factors
    )
    entries.append(new_entry)
    return new_entry


def find_entry_by_id(
    entries: List[MoodEntry],
    entry_id: int,
) -> Optional[MoodEntry]:
    """Ищет запись по её уникальному идентификатору."""
    for entry in entries:
        if entry.id == entry_id:
            return entry
    return None


def find_entries_by_date(
    entries: List[MoodEntry],
    target_date: date,
) -> List[MoodEntry]:
    """Возвращает все записи за указанную дату."""
    return [entry for entry in entries if entry.entry_date == target_date]


def filter_entries_by_score(
    entries: List[MoodEntry],
    min_score: int,
) -> List[MoodEntry]:
    """Фильтрует записи, оставляя только те, где оценка >= min_score."""
    return [entry for entry in entries if entry.score >= min_score]


def sort_entries_by_score(
    entries: List[MoodEntry],
    reverse: bool = False,
) -> List[MoodEntry]:
    """Сортирует записи по оценке настроения."""
    return sorted(
        entries,
        key=lambda entry: entry.score,
        reverse=reverse,
    )


def get_average_mood(entries: List[MoodEntry]) -> float:
    """Вычисляет среднюю оценку настроения."""
    if not entries:
        return 0.0
    total = sum(entry.score for entry in entries)
    return round(total / len(entries), 1)


def get_mood_trend(entries: List[MoodEntry], last_n: int = 3) -> str:
    """Определяет тенденцию изменения настроения за последние N записей."""
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
