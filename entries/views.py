from django.http import HttpResponse

from homepage.views import page
from models.entries import find_entry_by_id
from storage import load_entries, load_factors, load_moods, load_users


def _get_score_badge(score: int) -> str:
    """Возвращает CSS-класс бейджа Bootstrap в зависимости от оценки."""
    if score >= 7:
        return "bg-success"
    elif score >= 4:
        return "bg-warning text-dark"
    return "bg-danger"


def entries(request):
    """Отображает список записей настроения."""
    users = load_users("data/users.json")
    moods_list = load_moods("data/moods.json")
    factors = load_factors("data/factors.json")
    entries_list = load_entries(
        "data/entries.json", users, moods_list, factors
    )

    items = ""
    for entry in entries_list:
        badge = _get_score_badge(entry.score)
        status = entry.get_status()
        items += f"""
        <li class="list-group-item d-flex justify-content-between
                   align-items-center">
            <a href="/entries/{entry.id}/">
                {entry.entry_date} — {entry.user.name} ({entry.score}/10)
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """

    content = f"""
    <h1>Записи настроения</h1>
    <p class="text-muted">Всего записей: {len(entries_list)}</p>
    <ul class="list-group">
        {items}
    </ul>
    """
    return HttpResponse(page("Mood Tracker — Записи", content))


def entry_detail(request, entry_id):
    """Отображает детальную информацию об одной записи настроения."""
    users = load_users("data/users.json")
    moods_list = load_moods("data/moods.json")
    factors = load_factors("data/factors.json")
    entries_list = load_entries(
        "data/entries.json", users, moods_list, factors
    )

    entry = find_entry_by_id(entries_list, entry_id)
    if entry is None:
        content = """
        <h1 class="text-danger">Запись не найдена</h1>
        <p>Запись с указанным идентификатором отсутствует в системе.</p>
        <a href="/entries/" class="btn btn-outline-secondary">
            ← к списку записей
        </a>
        """
        return HttpResponse(
            page("Запись не найдена", content),
            status=404,
        )

    badge = _get_score_badge(entry.score)
    mood_info = entry.mood.name if entry.mood else "Не указано"
    if entry.factors:
        factors_info = ", ".join(f.name for f in entry.factors)
    else:
        factors_info = "Не указаны"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                Запись №{entry.id} от {entry.entry_date}
            </h5>
            <p class="card-text">
                <strong>Пользователь:</strong> {entry.user.name}
            </p>
            <p class="card-text">
                <strong>Оценка настроения:</strong> {entry.score}/10
            </p>
            <p class="card-text">
                <strong>Статус дня:</strong>
                <span class="badge {badge}">{entry.get_status()}</span>
            </p>
            <p class="card-text">
                <strong>Тип настроения:</strong> {mood_info}
            </p>
            <p class="card-text">
                <strong>Факторы влияния:</strong> {factors_info}
            </p>
            <p class="card-text">
                <strong>Комментарий:</strong> {entry.comment}
            </p>
            <a href="/entries/" class="btn btn-outline-secondary">
                ← к списку записей
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Запись №{entry.id}", content),
        status=200,
    )
