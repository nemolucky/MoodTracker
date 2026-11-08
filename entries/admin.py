"""Администрирование дневника и связанных записей."""
from django.contrib import admin
from .models import MoodEntry, User


class EntryInline(admin.TabularInline):
    model = MoodEntry
    extra = 0
    show_change_link = True
    fields = ("user", "mood", "entry_date", "score",
              "publication_status", "comment")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    search_fields = ("name", "email")
    ordering = ("name", "pk")
    list_per_page = 25
    inlines = (EntryInline,)


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "entry_date", "user", "mood", "score",
                    "publication_status")
    list_filter = ("publication_status", "mood", "entry_date")
    search_fields = ("comment", "user__name", "mood__name")
    ordering = ("-entry_date", "-pk")
    list_select_related = ("user", "mood")
    list_per_page = 25
    date_hierarchy = "entry_date"
    filter_horizontal = ("factors",)


admin.site.site_header = "Управление дневником настроения"
admin.site.site_title = "Mood Tracker"
admin.site.index_title = "Данные приложения"
