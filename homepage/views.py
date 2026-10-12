from django.http import HttpResponse


def page(title, content):
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav border-bottom p-2 mb-4 bg-light">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/entries/">Записи</a>
        <a class="nav-link" href="/moods/">Настроения</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    content = """
    <h1 class="display-4">Mood Tracker</h1>
    <p class="lead">
        Дневник эмоционального состояния и отслеживания настроения.
    </p>
    <p>Основные разделы:</p>
    <a href="/entries/" class="btn btn-primary me-2">Записи настроения</a>
    <a href="/moods/" class="btn btn-secondary">Типы настроения</a>
    """
    return HttpResponse(page("Mood Tracker — Главная", content))


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
