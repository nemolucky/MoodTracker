"""Справочник настроений и обратные связи ORM."""
from django.shortcuts import render
from .models import Mood


def moods(request):
    query = request.GET.get("q", "").strip()[:200]
    rows = Mood.objects.all().order_by("name")
    if query:
        rows = rows.filter(name__icontains=query)
    return render(request, "moods/mood_list.html", {
        "moods": rows, "query": query})


def mood_detail(request, mood_id=None, slug=None):
    lookup = {"slug": slug} if slug else {"pk": mood_id}
    mood = Mood.objects.filter(**lookup).first()
    related = mood.entries.published().with_relations().order_by(
        "-entry_date", "-pk") if mood else []
    return render(request, "moods/mood_detail.html", {
        "mood": mood, "related_entries": related},
        status=200 if mood else 404)
