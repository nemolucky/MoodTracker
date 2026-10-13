from django.shortcuts import render

from models.moods import find_mood_by_id
from storage import load_entries, load_factors, load_moods, load_users


def moods(request):
    """Отображает список типов настроения."""
    moods_list = load_moods("data/moods.json")
    context = {
        "moods": moods_list,
    }
    return render(request, "moods/mood_list.html", context)


def mood_detail(request, mood_id):
    """Отображает информацию о настроении и связанные записи."""
    moods_list = load_moods("data/moods.json")
    mood = find_mood_by_id(moods_list, mood_id)

    related = []
    if mood is not None:
        users = load_users("data/users.json")
        factors = load_factors("data/factors.json")
        entries_list = load_entries(
            "data/entries.json", users, moods_list, factors
        )
        related = [e for e in entries_list if e.mood and e.mood.id == mood.id]

    context = {
        "mood": mood,
        "related_entries": related,
    }
    return render(
        request,
        "moods/mood_detail.html",
        context,
        status=404 if mood is None else 200,
    )
