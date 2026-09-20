from datetime import date


def input_int(prompt: str, min_value: int = 0, max_value: int = 10) -> int:
    while True:
        raw_value = input(prompt)
        try:
            value = int(raw_value)
        except ValueError:
            print("Ошибка: введите целое число.")
            continue
        if value < min_value or value > max_value:
            print(f"Ошибка: число должно быть от {min_value} до {max_value}.")
            continue
        return value


def input_date(prompt: str) -> date:
    while True:
        raw_value = input(prompt)
        try:
            return date.fromisoformat(raw_value)
        except ValueError:
            print(
                "Ошибка: введите дату в формате ГГГГ-ММ-ДД, "
                "например 2026-09-15."
            )
