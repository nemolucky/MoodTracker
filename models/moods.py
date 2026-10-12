"""Модель для сущности Mood (Тип настроения)."""
from typing import Any, Dict, List, Optional


class Mood:
    """Представляет тип настроения (например, Радость, Грусть, Спокойствие)."""

    def __init__(
        self, mood_id: int, name: str, description: str = ""
    ) -> None:
        self.id = mood_id
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return f"{self.name}"

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "Mood":
        return cls(
            mood_id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
        )


def add_mood(
    moods: List[Mood], mood_id: int, name: str, description: str = ""
) -> Mood:
    new_mood = Mood(mood_id, name, description)
    moods.append(new_mood)
    return new_mood


def find_mood_by_id(moods: List[Mood], mood_id: int) -> Optional[Mood]:
    for mood in moods:
        if mood.id == mood_id:
            return mood
    return None


def find_mood_by_name(moods: List[Mood], name: str) -> Optional[Mood]:
    name_lower = name.lower()
    for mood in moods:
        if mood.name.lower() == name_lower:
            return mood
    return None
