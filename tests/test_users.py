"""Тесты для класса User и функций модуля models/users.py."""
from models.users import User, add_user, find_user, find_user_by_id


def test_user_creation():
    user = User(1, "Denis", "denis@example.com")
    assert user.id == 1
    assert user.name == "Denis"
    assert user.email == "denis@example.com"


def test_user_str_with_email():
    user = User(1, "Denis", "denis@example.com")
    assert str(user) == "Denis (denis@example.com)"


def test_user_str_without_email():
    user = User(1, "Denis")
    assert str(user) == "Denis"


def test_user_from_data():
    data = {"id": 2, "name": "Anna", "email": "anna@example.com"}
    user = User.from_data(data)
    assert user.id == 2
    assert user.name == "Anna"
    assert user.email == "anna@example.com"


def test_add_user():
    users = []
    add_user(users, 1, "Denis", "denis@example.com")
    assert len(users) == 1
    assert users[0].name == "Denis"


def test_find_user_by_id():
    users = [User(1, "Denis"), User(2, "Anna")]
    found = find_user_by_id(users, 2)
    assert found is not None
    assert found.name == "Anna"


def test_find_user_by_id_not_found():
    users = [User(1, "Denis")]
    assert find_user_by_id(users, 99) is None


def test_find_user_by_query():
    users = [
        User(1, "Denis", "denis@example.com"),
        User(2, "Anna", "anna@example.com"),
    ]
    found = find_user(users, "anna")
    assert len(found) == 1
    assert found[0].name == "Anna"