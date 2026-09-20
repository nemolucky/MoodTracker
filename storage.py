import json
from datetime import date
from typing import Any, Dict, List


def load_entries(filename: str) -> List[Dict[str, Any]]:
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
        entries.append({
            "entry_date": date.fromisoformat(raw_entry["entry_date"]),
            "score": raw_entry["score"],
            "comment": raw_entry["comment"],
        })
    return entries


def save_entries(filename: str, entries: List[Dict[str, Any]]) -> None:
    raw_entries = [
        {
            "entry_date": entry["entry_date"].isoformat(),
            "score": entry["score"],
            "comment": entry["comment"],
        }
        for entry in entries
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_entries, file, ensure_ascii=False, indent=4)