"""Точка входа в приложение Mood Tracker (объектная модель)."""
from typing import List, Optional

from models import MoodEntry, User
from models.entries import (
    filter_entries_by_score,
    find_entries_by_date,
    get_average_mood,
    get_mood_trend,
    sort_entries_by_score,
)
from models.factors import Factor, add_factor, find_factor_by_id
from models.moods import Mood, add_mood, find_mood_by_id
from models.users import add_user, find_user_by_id
from storage import (
    load_entries,
    load_factors,
    load_moods,
    load_users,
    save_entries,
    save_factors,
    save_moods,
    save_users,
)
from utils import input_date, input_int

ENTRIES_FILE = "data/entries.json"
USERS_FILE = "data/users.json"
MOODS_FILE = "data/moods.json"
FACTORS_FILE = "data/factors.json"

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
    "9. Управление настроениями\n"
    "10. Управление факторами\n"
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


def show_moods(moods: List[Mood]) -> None:
    """Вывести список типов настроения."""
    if not moods:
        print("Список настроений пуст.")
        return
    for mood in moods:
        print(f"{mood.id}. {mood.name} - {mood.description}")


def show_factors(factors: List[Factor]) -> None:
    """Вывести список факторов."""
    if not factors:
        print("Список факторов пуст.")
        return
    for factor in factors:
        print(f"{factor.id}. {factor.name} ({factor.category})")


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


def get_next_mood_id(moods: List[Mood]) -> int:
    if not moods:
        return 1
    return max(m.id for m in moods) + 1


def get_next_factor_id(factors: List[Factor]) -> int:
    if not factors:
        return 1
    return max(f.id for f in factors) + 1


def select_mood(moods: List[Mood]) -> Optional[Mood]:
    """Помощник для выбора настроения из списка."""
    if not moods:
        print("Настроения еще не добавлены.")
        return None

    print("\nДоступные типы настроения:")
    for m in moods:
        print(f"{m.id}. {m.name}")

    mood_id = input_int(
        "Выберите ID настроения (0, если не указано): ", 0, 999
    )
    if mood_id == 0:
        return None
    return find_mood_by_id(moods, mood_id)


def select_factors(factors: List[Factor]) -> List[Factor]:
    """Помощник для выбора нескольких факторов."""
    if not factors:
        print("Факторы еще не добавлены.")
        return []

    print("\nДоступные факторы:")
    for f in factors:
        print(f"{f.id}. {f.name} ({f.category})")

    selected = []
    while True:
        fid = input_int(
            "Выберите ID фактора (0 для завершения выбора): ", 0, 999
        )
        if fid == 0:
            break
        factor = find_factor_by_id(factors, fid)
        if factor:
            if factor not in selected:
                selected.append(factor)
            else:
                print("Этот фактор уже выбран.")
        else:
            print("Фактор с таким ID не найден.")
    return selected


def create_new_entry(
    entries: List[MoodEntry],
    users: List[User],
    moods: List[Mood],
    factors: List[Factor],
) -> None:
    """Создать новую запись настроения."""
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

    # Выбор настроения и факторов
    mood = select_mood(moods)
    selected_factors = select_factors(factors)

    entry_id = get_next_entry_id(entries)
    # Передаем новые аргументы в конструктор
    new_entry = MoodEntry(
        entry_id, entry_date, score, comment, user, mood, selected_factors
    )
    entries.append(new_entry)
    print(f"Добавлена запись: {new_entry}")


def manage_moods(moods: List[Mood]) -> None:
    """Простое управление списком настроений."""
    while True:
        print("\n--- Управление настроениями ---")
        show_moods(moods)
        print("1. Добавить настроение")
        print("0. Назад")
        choice = input("Выбор: ")

        if choice == "1":
            name = input("Название настроения: ")
            desc = input("Описание (можно пропустить): ")
            add_mood(moods, get_next_mood_id(moods), name, desc)
        elif choice == "0":
            break


def manage_factors(factors: List[Factor]) -> None:
    """Простое управление списком факторов."""
    while True:
        print("\n--- Управление факторами ---")
        show_factors(factors)
        print("1. Добавить фактор")
        print("0. Назад")
        choice = input("Выбор: ")

        if choice == "1":
            name = input("Название фактора: ")
            cat = input("Категория (например, Работа, Здоровье): ")
            add_factor(factors, get_next_factor_id(factors), name, cat)
        elif choice == "0":
            break


def main() -> None:
    """Запустить главное меню приложения."""
    # Загрузка данных
    users = load_users(USERS_FILE)
    if not users:
        users = [User(1, "Denis", "")]

    # Загрузка новых сущностей ДО загрузки записей
    moods = load_moods(MOODS_FILE)
    factors = load_factors(FACTORS_FILE)

    # Теперь передаем moods и factors в load_entries
    entries = load_entries(ENTRIES_FILE, users, moods, factors)

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_entries(entries)

        elif choice == "2":
            create_new_entry(entries, users, moods, factors)
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

        elif choice == "9":
            manage_moods(moods)
            save_moods(MOODS_FILE, moods)

        elif choice == "10":
            manage_factors(factors)
            save_factors(FACTORS_FILE, factors)

        elif choice == "0":
            save_entries(ENTRIES_FILE, entries)
            save_users(USERS_FILE, users)
            save_moods(MOODS_FILE, moods)
            save_factors(FACTORS_FILE, factors)
            print("Данные сохранены. До встречи!")
            break

        else:
            print("Неизвестная команда, попробуйте снова.")


if __name__ == "__main__":
    main()
