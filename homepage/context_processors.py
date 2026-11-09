"""Общие данные интерфейса без дополнительных запросов к БД."""


def site_info(request):
    return {"site_name": "Mood Tracker", "site_description":
            "Дневник эмоционального состояния"}
