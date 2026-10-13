from django.shortcuts import render

from models.entries import find_entry_by_id
from storage import load_entries, load_factors, load_moods, load_users


def entries(request):
    """Отображает список записей настроения."""
    users = load_users("data/users.json")
    moods_list = load_moods("data/moods.json")
    factors = load_factors("data/factors.json")
    entries_list = load_entries(
        "data/entries.json", users, moods_list, factors
    )
    context = {
        "entries": entries_list,
    }
    return render(request, "entries/entry_list.html", context)


def entry_detail(request, entry_id):
    """Отображает детальную информацию об одной записи настроения."""
    users = load_users("data/users.json")
    moods_list = load_moods("data/moods.json")
    factors = load_factors("data/factors.json")
    entries_list = load_entries(
        "data/entries.json", users, moods_list, factors
    )

    entry = find_entry_by_id(entries_list, entry_id)
    context = {
        "entry": entry,
    }
    return render(
        request,
        "entries/entry_detail.html",
        context,
        status=404 if entry is None else 200,
    )
