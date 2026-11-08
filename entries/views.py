"""Списки, поиск и аналитика дневника через Django ORM."""
from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Min, Q
from django.db.models.functions import Round
from django.shortcuts import render

from moods.models import Factor, Mood
from .forms import EntryFilterForm
from .models import MoodEntry


SORTS = {"": ("-entry_date", "-pk"), "date": ("entry_date", "pk"),
         "score": ("-score", "-entry_date", "-pk"),
         "user": ("user__name", "-entry_date", "-pk")}


def entries(request):
    form = EntryFilterForm(request.GET)
    rows = MoodEntry.objects.published().with_relations()
    if form.is_valid():
        data = form.cleaned_data
        if data["date"]:
            rows = rows.on_date(data["date"])
        if data["mood"]:
            rows = rows.filter(mood=data["mood"])
        if data["min_score"] is not None:
            rows = rows.filter(score__gte=data["min_score"])
        if data["q"]:
            rows = rows.filter(
                Q(comment__icontains=data["q"]) |
                Q(user__name__icontains=data["q"]) |
                Q(mood__name__icontains=data["q"]))
        rows = rows.order_by(*SORTS[data["sort"]])
    else:
        rows = rows.none()
    page = Paginator(rows, 3).get_page(request.GET.get("page"))
    return render(request, "entries/entry_list.html", {
        "entries": page, "page_obj": page, "form": form})


def entry_detail(request, entry_id):
    entry = (MoodEntry.objects.published().with_relations()
             .prefetch_related("factors").filter(pk=entry_id).first())
    return render(request, "entries/entry_detail.html", {
        "entry": entry, "factors": entry.factors.all() if entry else []},
        status=200 if entry else 404)


def search_by_date(request):
    form = EntryFilterForm(request.GET)
    found, unused = MoodEntry.objects.none(), Mood.objects.none()
    if form.is_valid() and form.cleaned_data["date"]:
        date = form.cleaned_data["date"]
        found = MoodEntry.objects.published().on_date(date).select_related(
            "user", "mood").order_by("pk")
        used = found.exclude(mood=None).values_list("mood_id", flat=True)
        unused = Mood.objects.exclude(pk__in=used).order_by("name")
    return render(request, "entries/search.html", {
        "search_date": request.GET.get("date", ""), "entries": found,
        "unused_moods": unused, "errors": form.errors})


def statistics(request):
    overall = MoodEntry.objects.published().aggregate(
        total_entries=Count("pk"), avg_score=Round(Avg("score"), 1),
        min_score=Min("score"), max_score=Max("score"))
    moods = Mood.objects.annotate(
        mood_id=F("pk"), mood_name=F("name"),
        entries_count=Count("entries", filter=Q(
            entries__publication_status=MoodEntry.Status.PUBLISHED)),
        avg_score=Round(Avg("entries__score", filter=Q(
            entries__publication_status=MoodEntry.Status.PUBLISHED)), 1)
    ).order_by("-entries_count", "name")
    categories = Factor.objects.values("category").annotate(
        factors_count=Count("pk")).order_by("-factors_count", "category")
    return render(request, "entries/statistics.html", {
        "overall": overall, "mood_stats": moods,
        "category_stats": categories,
        "status_stats": MoodEntry.objects.values(
            "publication_status").annotate(
            entries_count=Count("pk")).order_by("publication_status")})
