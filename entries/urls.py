"""Маршруты для приложения записей настроения (entries)."""
from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("create/", views.entry_create, name="create"),
    path("<int:entry_id>/edit/", views.entry_edit, name="edit"),
    path("<int:entry_id>/archive/", views.entry_archive, name="archive"),
    path("", views.entries, name="list"),
    path("<int:entry_id>/", views.entry_detail, name="detail"),
    path("search/", views.search_by_date, name="search"),
    path("statistics/", views.statistics, name="statistics"),
]
