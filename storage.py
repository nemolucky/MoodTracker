import json
from datetime import date
from typing import List

from models import MoodEntry, User
from models.users import find_user_by_id


def load_users(filename: str) -> List[User]:
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
    raw_users = [
        {"id": user.id, "name": user.name, "email": user.email}
        for user in users
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_users, file, ensure_ascii=False, indent=4)


def load_entries(filename: str, users: List[User]) -> List[MoodEntry]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_entries = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Начинаем с пустого списка.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён. Начинаем с пустого списка.")
        return []

    entries = []
    for raw_entry in raw_entries:
        user = find_user_by_id(users, raw_entry["user_id"])
        if user is None:
            print(
                f"Пользователь с id={raw_entry['user_id']} не найден, "
                f"запись id={raw_entry['id']} пропущена."
            )
            continue
        entries.append(MoodEntry(
            entry_id=raw_entry["id"],
            entry_date=date.fromisoformat(raw_entry["entry_date"]),
            score=raw_entry["score"],
            comment=raw_entry["comment"],
            user=user,
        ))
    return entries


def save_entries(filename: str, entries: List[MoodEntry]) -> None:
    raw_entries = [
        {
            "id": entry.id,
            "user_id": entry.user.id,
            "entry_date": entry.entry_date.isoformat(),
            "score": entry.score,
            "comment": entry.comment,
        }
        for entry in entries
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_entries, file, ensure_ascii=False, indent=4)