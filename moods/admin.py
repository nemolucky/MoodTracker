"""Настройки справочников в Django Admin."""
from django.contrib import admin
from entries.admin import EntryInline
from .models import Factor, Mood


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "description")
    ordering = ("name", "pk")
    list_per_page = 25
    inlines = (EntryInline,)


@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)
    search_fields = ("name", "category")
    ordering = ("category", "name", "pk")
    list_per_page = 25
