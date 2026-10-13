from django.shortcuts import render


def index(request):
    """Главная страница сервиса."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception=None):
    """Кастомный обработчик ошибки 404."""
    return render(request, "404.html", status=404)
