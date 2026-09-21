from typing import Any, Dict, List, Optional


class User:

    def __init__(
        self,
        user_id: int,
        name: str,
        email: str = "",
    ) -> None:
        self.id = user_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        if self.email:
            return f"{self.name} ({self.email})"
        return self.name

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "User":
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data.get("email", ""),
        )


def add_user(
    users: List[User],
    user_id: int,
    name: str,
    email: str = "",
) -> User:
    new_user = User(user_id, name, email)
    users.append(new_user)
    return new_user


def find_user_by_id(users: List[User], user_id: int) -> Optional[User]:
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_user(users: List[User], query: str) -> List[User]:
    query_lower = query.lower()
    return [
        user for user in users
        if query_lower in user.name.lower()
        or query_lower in user.email.lower()
    ]
