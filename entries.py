from datetime import date
from typing import Any, Dict, List


def add_mood_entry(
    entries: List[Dict[str, Any]],
    entry_date: date,
    score: int,
    comment: str,
) -> Dict[str, Any]:

    new_entry = {
        "entry_date": entry_date,
        "score": score,
        "comment": comment,
    }
    entries.append(new_entry)
    return new_entry


def get_day_status(score: float) -> str:
    if score >= 7:
        return "Хороший день"
    elif score >= 4:
        return "Нейтральный день"
    return "Плохой день"


def get_average_mood(entries: List[Dict[str, Any]]) -> float:
    if not entries:
        return 0.0
    total = sum(entry["score"] for entry in entries)
    return round(total / len(entries), 1)


def find_entries_by_date(
    entries: List[Dict[str, Any]],
    target_date: date,
) -> List[Dict[str, Any]]:
    return [
        entry for entry in entries
        if entry["entry_date"] == target_date
    ]


def filter_entries_by_score(
    entries: List[Dict[str, Any]],
    min_score: int,
) -> List[Dict[str, Any]]:
    return [entry for entry in entries if entry["score"] >= min_score]


def sort_entries_by_score(
    entries: List[Dict[str, Any]],
    reverse: bool = False,
) -> List[Dict[str, Any]]:
    return sorted(
        entries,
        key=lambda entry: entry["score"],
        reverse=reverse,
    )


def get_mood_trend(
    entries: List[Dict[str, Any]],
    last_n: int = 3,
) -> str:

    if len(entries) < last_n * 2:
        return "Недостаточно данных для оценки тенденции"

    sorted_by_date = sorted(entries, key=lambda entry: entry["entry_date"])
    recent = sorted_by_date[-last_n:]
    previous = sorted_by_date[-last_n * 2:-last_n]

    recent_avg = get_average_mood(recent)
    previous_avg = get_average_mood(previous)

    if recent_avg > previous_avg:
        return "Настроение улучшается"
    elif recent_avg < previous_avg:
        return "Настроение ухудшается"
    return "Настроение стабильно"