"""Тесты для Django-представлений (views) и маршрутов проекта."""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moodtracker.settings")
django.setup()

from django.test import Client, override_settings, RequestFactory  # noqa: E402
from homepage.views import page_not_found  # noqa: E402


def test_homepage_view():
    """Главная страница возвращает статус 200 и базовые ссылки."""
    client = Client()
    response = client.get("/")
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Mood Tracker" in content
    assert 'href="/entries/"' in content
    assert 'href="/moods/"' in content


def test_entries_list_view():
    """Список записей возвращает статус 200 и содержит заголовок."""
    client = Client()
    response = client.get("/entries/")
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Записи настроения" in content


def test_entry_detail_success():
    """Существующая запись возвращает статус 200 и карточку записи."""
    client = Client()
    response = client.get("/entries/1/")
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Запись №1" in content


def test_entry_detail_not_found():
    """Несуществующая запись возвращает статус 404."""
    client = Client()
    response = client.get("/entries/9999/")
    assert response.status_code == 404
    content = response.content.decode("utf-8")
    assert "Запись не найдена" in content


def test_moods_list_view():
    """Список типов настроения возвращает статус 200."""
    client = Client()
    response = client.get("/moods/")
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Типы настроения" in content


def test_mood_detail_success():
    """Существующий тип настроения возвращает статус 200."""
    client = Client()
    response = client.get("/moods/1/")
    assert response.status_code == 200


def test_mood_detail_not_found():
    """Несуществующий тип настроения возвращает статус 404."""
    client = Client()
    response = client.get("/moods/9999/")
    assert response.status_code == 404
    content = response.content.decode("utf-8")
    assert "Настроение не найдено" in content


def test_custom_404_handler_with_debug_false():
    """При DEBUG=False несуществующий URL отдаёт кастомную 404."""
    client = Client()
    with override_settings(DEBUG=False):
        response = client.get("/nonexistent-page/")
        assert response.status_code == 404
        content = response.content.decode("utf-8")
        assert "404 — страница не найдена" in content


def test_page_not_found_view_directly():
    """Прямой вызов view-функции page_not_found отдаёт 404."""
    factory = RequestFactory()
    request = factory.get("/test-404/")
    response = page_not_found(request, exception=None)
    assert response.status_code == 404
    content = response.content.decode("utf-8")
    assert "404 — страница не найдена" in content
