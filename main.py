"""Точка входа в приложение Mood Tracker (объектная модель)."""
from typing import List

from models import MoodEntry, User
from models.entries import (
    filter_entries_by_score,
    find_entries_by_date,
    get_average_mood,
    get_mood_trend,
    sort_entries_by_score,
)
from models.users import add_user, find_user_by_id
from storage import load_entries, load_users, save_entries, save_users
from utils import input_date, input_int

ENTRIES_FILE = "data/entries.json"
USERS_FILE = "data/users.json"

MENU = (
    "\n=== Mood Tracker ===\n"
    "1. Показать записи\n"
    "2. Добавить запись\n"
    "3. Найти записи по дате\n"
    "4. Показать средний балл и тенденцию\n"
    "5. Отфильтровать по минимальной оценке\n"
    "6. Показать записи, отсортированные по оценке\n"
    "7. Показать пользователей\n"
    "8. Добавить пользователя\n"
    "0. Выход"
)


def show_entries(entries: List[MoodEntry]) -> None:
    """Вывести список записей настроения."""
    if not entries:
        print("Записей пока нет.")
        return
    for entry in entries:
        print(entry)
        print(f"  Комментарий: {entry.comment}")


def show_users(users: List[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Пользователей пока нет.")
        return
    for user in users:
        print(f"{user.id}: {user}")


def show_summary(entries: List[MoodEntry]) -> None:
    """Вывести средний балл и тенденцию настроения."""
    average = get_average_mood(entries)
    print(f"Средний балл настроения: {average}/10")
    print(get_mood_trend(entries))


def get_next_entry_id(entries: List[MoodEntry]) -> int:
    """Вычислить идентификатор для новой записи."""
    if not entries:
        return 1
    return max(entry.id for entry in entries) + 1


def get_next_user_id(users: List[User]) -> int:
    """Вычислить идентификатор для нового пользователя."""
    if not users:
        return 1
    return max(user.id for user in users) + 1


def create_new_entry(entries: List[MoodEntry], users: List[User]) -> None:
    """Создать новую запись настроения, связав её с пользователем."""
    show_users(users)
    user_id = input_int(
        "ID пользователя (0, если нужно создать нового): ",
        min_value=0,
        max_value=999,
    )
    user = find_user_by_id(users, user_id)
    if user is None:
        name = input("Имя нового пользователя: ")
        email = input("Email (можно пропустить): ")
        user = add_user(users, get_next_user_id(users), name, email)
        print(f"Создан пользователь: {user}")

    entry_date = input_date("Дата записи (ГГГГ-ММ-ДД): ")
    score = input_int("Оценка (0-10): ")
    comment = input("Комментарий: ")

    entry_id = get_next_entry_id(entries)
    new_entry = MoodEntry(entry_id, entry_date, score, comment, user)
    entries.append(new_entry)
    print(f"Добавлена запись: {new_entry}")


def main() -> None:
    """Запустить главное меню приложения."""
    users = load_users(USERS_FILE)
    if not users:
        users = [User(1, "Denis", "")]

    entries = load_entries(ENTRIES_FILE, users)

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_entries(entries)

        elif choice == "2":
            create_new_entry(entries, users)
            save_entries(ENTRIES_FILE, entries)
            save_users(USERS_FILE, users)

        elif choice == "3":
            target_date = input_date("Дата для поиска (ГГГГ-ММ-ДД): ")
            show_entries(find_entries_by_date(entries, target_date))

        elif choice == "4":
            show_summary(entries)

        elif choice == "5":
            min_score = input_int("Минимальная оценка: ")
            show_entries(filter_entries_by_score(entries, min_score))

        elif choice == "6":
            show_entries(sort_entries_by_score(entries, reverse=True))

        elif choice == "7":
            show_users(users)

        elif choice == "8":
            name = input("Имя пользователя: ")
            email = input("Email (можно пропустить): ")
            user = add_user(users, get_next_user_id(users), name, email)
            print(f"Добавлен пользователь: {user}")
            save_users(USERS_FILE, users)

        elif choice == "0":
            save_entries(ENTRIES_FILE, entries)
            save_users(USERS_FILE, users)
            print("Данные сохранены. До встречи!")
            break

        else:
            print("Неизвестная команда, попробуйте снова.")


if __name__ == "__main__":
    main()