from typing import Any, Dict, List

from entries import (
    add_mood_entry,
    filter_entries_by_score,
    find_entries_by_date,
    get_average_mood,
    get_day_status,
    get_mood_trend,
    sort_entries_by_score,
)
from storage import load_entries, save_entries
from utils import input_date, input_int

DATA_FILE = "data/entries.json"
USER_NAME = "Denis"

MENU = (
    "\n=== Mood Tracker ===\n"
    "1. Показать записи\n"
    "2. Добавить запись\n"
    "3. Найти записи по дате\n"
    "4. Показать средний балл и тенденцию\n"
    "5. Отфильтровать по минимальной оценке\n"
    "6. Показать записи, отсортированные по оценке\n"
    "0. Выход"
)


def show_entries(entries: List[Dict[str, Any]]) -> None:
    if not entries:
        print("Записей пока нет.")
        return
    for entry in entries:
        status = get_day_status(entry["score"])
        print(f"{entry['entry_date']} | Оценка: {entry['score']}/10 | {status}")
        print(f"  Комментарий: {entry['comment']}")


def show_summary(entries: List[Dict[str, Any]]) -> None:
    average = get_average_mood(entries)
    print(f"Средний балл настроения: {average}/10")
    print(f"Общая тенденция: {get_day_status(average)}")
    print(get_mood_trend(entries))


def main() -> None:
    entries = load_entries(DATA_FILE)
    print(f"Пользователь: {USER_NAME}")

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_entries(entries)

        elif choice == "2":
            entry_date = input_date("Дата записи (ГГГГ-ММ-ДД): ")
            score = input_int("Оценка (0-10): ")
            comment = input("Комментарий: ")
            new_entry = add_mood_entry(entries, entry_date, score, comment)
            save_entries(DATA_FILE, entries)
            print(
                f"Добавлена запись: {new_entry['entry_date']} | "
                f"Оценка: {new_entry['score']}/10"
            )

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

        elif choice == "0":
            save_entries(DATA_FILE, entries)
            print("Данные сохранены. До встречи!")
            break

        else:
            print("Неизвестная команда, попробуйте снова.")


if __name__ == "__main__":
    main()