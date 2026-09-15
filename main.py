from datetime import date

mood_entries = [
    {"entry_date": date(2026, 9, 13), "score": 8, "comment": "Отличная встреча с друзьями"},
    {"entry_date": date(2026, 9, 14), "score": 5, "comment": "Обычный рабочий день"},
    {"entry_date": date(2026, 9, 15), "score": 3, "comment": "Много задач, устал"},
]

user_name = "Denis"


def add_mood_entry(entries, entry_date, score, comment):
    new_entry = {
        "entry_date": entry_date,
        "score": score,
        "comment": comment,
    }
    entries.append(new_entry)
    return new_entry


def get_day_status(score):
    if score >= 7:
        return "Хороший день"
    elif score >= 4:
        return "Нейтральный день"
    else:
        return "Плохой день"


def get_average_mood(entries):
    if not entries:
        return 0.0
    total = sum(entry["score"] for entry in entries)
    average = total / len(entries)
    return round(average, 1)



print(f"Пользователь: {user_name}")
print("-" * 30)

for entry in mood_entries:
    status = get_day_status(entry["score"])
    print(f"{entry['entry_date']} | Оценка: {entry['score']}/10 | {status}")
    print(f"  Комментарий: {entry['comment']}")

print("-" * 30)

new_entry = add_mood_entry(
    mood_entries,
    date(2026, 9, 16),
    9,
    "Каникулы!"
)
print(f"Добавлена новая запись: {new_entry['entry_date']} | Оценка: {new_entry['score']}/10")

average = get_average_mood(mood_entries)
print(f"Средний балл настроения: {average}/10")
print(f"Общая тенденция: {get_day_status(average)}")