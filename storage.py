"""Модуль для сохранения и загрузки данных приложения Mood Tracker."""
import json
from datetime import date
from typing import List

from models import MoodEntry, User
from models.factors import Factor
from models.moods import Mood
from models.users import find_user_by_id


def load_users(filename: str) -> List[User]:
    """Загружает список пользователей из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_users = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Начинаем с пустого списка.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён. Начинаем с пустого списка.")
        return []

    return [User.from_data(raw_user) for raw_user in raw_users]


def save_users(filename: str, users: List[User]) -> None:
    """Сохраняет список пользователей в JSON-файл."""
    raw_users = [
        {"id": user.id, "name": user.name, "email": user.email}
        for user in users
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_users, file, ensure_ascii=False, indent=4)


def load_moods(filename: str) -> List[Mood]:
    """Загружает список типов настроения из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_moods = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    return [Mood.from_data(raw_mood) for raw_mood in raw_moods]


def save_moods(filename: str, moods: List[Mood]) -> None:
    """Сохраняет список типов настроения в JSON-файл."""
    raw_moods = [
        {"id": mood.id, "name": mood.name, "description": mood.description}
        for mood in moods
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_moods, file, ensure_ascii=False, indent=4)


def load_factors(filename: str) -> List[Factor]:
    """Загружает список факторов из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_factors = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    return [Factor.from_data(raw_factor) for raw_factor in raw_factors]


def save_factors(filename: str, factors: List[Factor]) -> None:
    """Сохраняет список факторов в JSON-файл."""
    raw_factors = [
        {"id": factor.id, "name": factor.name, "category": factor.category}
        for factor in factors
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_factors, file, ensure_ascii=False, indent=4)


def load_entries(
    filename: str,
    users: List[User],
    moods: List[Mood],
    factors: List[Factor],
) -> List[MoodEntry]:
    """Загружает записи настроения со связями."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_entries = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    entries = []
    for raw_entry in raw_entries:
        # Восстановление пользователя
        user = find_user_by_id(users, raw_entry["user_id"])
        if user is None:
            continue

        # Восстановление настроения
        mood = None
        if raw_entry.get("mood_id"):
            from models.moods import find_mood_by_id
            mood = find_mood_by_id(moods, raw_entry["mood_id"])

        # Восстановление факторов
        entry_factors = []
        factor_ids = raw_entry.get("factor_ids", [])
        if factor_ids:
            from models.factors import find_factor_by_id
            for fid in factor_ids:
                f = find_factor_by_id(factors, fid)
                if f:
                    entry_factors.append(f)

        entries.append(MoodEntry(
            entry_id=raw_entry["id"],
            entry_date=date.fromisoformat(raw_entry["entry_date"]),
            score=raw_entry["score"],
            comment=raw_entry["comment"],
            user=user,
            mood=mood,
            factors=entry_factors,
        ))
    return entries


def save_entries(filename: str, entries: List[MoodEntry]) -> None:
    """Сохраняет записи настроения в JSON-файл."""
    raw_entries = []
    for entry in entries:
        raw_entry = {
            "id": entry.id,
            "user_id": entry.user.id,
            "entry_date": entry.entry_date.isoformat(),
            "score": entry.score,
            "comment": entry.comment,
        }

        # Сохраняем ID настроения, если оно есть
        if entry.mood:
            raw_entry["mood_id"] = entry.mood.id
        else:
            raw_entry["mood_id"] = None

        # Сохраняем список ID факторов
        raw_entry["factor_ids"] = [f.id for f in entry.factors]

        raw_entries.append(raw_entry)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_entries, file, ensure_ascii=False, indent=4)
