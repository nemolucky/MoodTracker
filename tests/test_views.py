"""Тесты для Django-представлений (views), шаблонов и маршрутов проекта."""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moodtracker.settings")
django.setup()

from django.test import Client, RequestFactory, override_settings  # noqa: E402
from django.urls import reverse  # noqa: E402
from homepage.views import page_not_found  # noqa: E402


def test_homepage_view():
    """Главная страница возвращает статус 200 и базовые ссылки."""
    client = Client()
    response = client.get(reverse("homepage:index"))
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Mood Tracker" in content
    assert reverse("entries:list") in content
    assert reverse("moods:list") in content


def test_static_assets_referenced():
    """Базовый шаблон подключает статические файлы проекта."""
    client = Client()
    response = client.get(reverse("homepage:index"))
    content = response.content.decode("utf-8")
    assert "/static/homepage/css/style.css" in content
    assert "/static/homepage/img/logo.png" in content
    assert "/static/homepage/js/main.js" in content
    assert 'id="current-year"' in content


def test_entries_list_view():
    """Список записей возвращает статус 200 и содержит заголовок."""
    client = Client()
    response = client.get(reverse("entries:list"))
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Записи настроения" in content
    assert "Всего записей:" in content


def test_entry_detail_success():
    """Существующая запись возвращает статус 200 и карточку записи."""
    client = Client()
    response = client.get(reverse("entries:detail", args=[1]))
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Запись №1" in content
    assert reverse("entries:list") in content


def test_entry_detail_not_found():
    """Несуществующая запись возвращает статус 404."""
    client = Client()
    response = client.get(reverse("entries:detail", args=[9999]))
    assert response.status_code == 404
    content = response.content.decode("utf-8")
    assert "Запись не найдена" in content


def test_moods_list_view():
    """Список типов настроения возвращает статус 200."""
    client = Client()
    response = client.get(reverse("moods:list"))
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Типы настроения" in content
    assert "Всего категорий:" in content


def test_mood_detail_success():
    """Существующий тип настроения возвращает статус 200."""
    client = Client()
    response = client.get(reverse("moods:detail", args=[1]))
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert reverse("moods:list") in content


def test_mood_detail_not_found():
    """Несуществующий тип настроения возвращает статус 404."""
    client = Client()
    response = client.get(reverse("moods:detail", args=[9999]))
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
