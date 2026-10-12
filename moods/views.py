from django.http import HttpResponse

from homepage.views import page
from models.moods import find_mood_by_id
from storage import load_entries, load_factors, load_moods, load_users


def moods(request):
    """Отображает список типов настроения."""
    moods_list = load_moods("data/moods.json")

    items = ""
    for mood in moods_list:
        items += f"""
        <li class="list-group-item d-flex justify-content-between
                   align-items-center">
            <a href="/moods/{mood.id}/">
                <strong>{mood.name}</strong>
            </a>
            <span class="text-muted">{mood.description}</span>
        </li>
        """

    content = f"""
    <h1>Типы настроения</h1>
    <ul class="list-group">
        {items}
    </ul>
    """
    return HttpResponse(page("Mood Tracker — Настроения", content))


def mood_detail(request, mood_id):
    """Отображает информацию о настроении и связанные записи."""
    moods_list = load_moods("data/moods.json")
    mood = find_mood_by_id(moods_list, mood_id)

    if mood is None:
        content = """
        <h1 class="text-danger">Настроение не найдено</h1>
        <p>Тип настроения с таким идентификатором не существует.</p>
        <a href="/moods/" class="btn btn-outline-secondary">
            ← к списку настроений
        </a>
        """
        return HttpResponse(
            page("Настроение не найдено", content),
            status=404,
        )

    users = load_users("data/users.json")
    factors = load_factors("data/factors.json")
    entries_list = load_entries(
        "data/entries.json", users, moods_list, factors
    )
    related = [e for e in entries_list if e.mood and e.mood.id == mood.id]

    entries_items = ""
    for entry in related:
        entries_items += f"""
        <li class="list-group-item">
            <a href="/entries/{entry.id}/">
                {entry.entry_date} — {entry.user.name} ({entry.score}/10)
            </a>
        </li>
        """

    if not entries_items:
        entries_items = (
            '<li class="list-group-item text-muted">'
            'Нет записей с этим настроением</li>'
        )

    content = f"""
    <div class="card mb-4">
        <div class="card-body">
            <h5 class="card-title">{mood.name}</h5>
            <p class="card-text">
                <strong>Описание:</strong> {mood.description}
            </p>
            <a href="/moods/" class="btn btn-outline-secondary">
                ← к списку настроений
            </a>
        </div>
    </div>
    <h4>Записи с этим настроением:</h4>
    <ul class="list-group">
        {entries_items}
    </ul>
    """
    return HttpResponse(
        page(mood.name, content),
        status=200,
    )
