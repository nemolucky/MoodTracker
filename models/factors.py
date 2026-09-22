"""Модель для сущности Factor (Фактор влияния)."""
from typing import Any, Dict, List, Optional

class Factor:
    """Представляет фактор, влияющий на настроение (например, Спорт, Работа, Погода)."""
    
    def __init__(self, factor_id: int, name: str, category: str = "Общее") -> None:
        self.id = factor_id
        self.name = name
        self.category = category

    def __str__(self) -> str:
        return f"{self.name} ({self.category})"

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "Factor":
        return cls(
            factor_id=data["id"],
            name=data["name"],
            category=data.get("category", "Общее"),
        )

def add_factor(factors: List[Factor], factor_id: int, name: str, category: str = "Общее") -> Factor:
    new_factor = Factor(factor_id, name, category)
    factors.append(new_factor)
    return new_factor

def find_factor_by_id(factors: List[Factor], factor_id: int) -> Optional[Factor]:
    for factor in factors:
        if factor.id == factor_id:
            return factor
    return None

def find_factors_by_category(factors: List[Factor], category: str) -> List[Factor]:
    category_lower = category.lower()
    return [f for f in factors if f.category.lower() == category_lower]