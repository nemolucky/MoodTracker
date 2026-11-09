"""Однократный атомарный перенос неизменяемого источника ПР7."""
import sqlite3
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from entries.models import MoodEntry, User
from moods.models import Factor, Mood


class Command(BaseCommand):
    help = "Переносит базу ПР7 в пустые таблицы ORM, сохраняя ID и связи"

    def add_arguments(self, parser):
        parser.add_argument(
            "--source", type=Path,
            default=settings.BASE_DIR / "data" / "moodtracker.sqlite")

    @transaction.atomic
    def handle(self, *args, **options):
        if any(m.objects.exists() for m in (User, Mood, Factor, MoodEntry)):
            raise CommandError("Таблицы ORM не пусты; импорт отменён")
        source = options["source"].resolve()
        try:
            conn = sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)
            conn.row_factory = sqlite3.Row
            try:
                data = {table: [dict(row) for row in conn.execute(
                    f"SELECT * FROM {table}")] for table in (
                        "users", "moods", "factors", "entries",
                        "entry_factors")}
            finally:
                conn.close()
            for table, model in (
                    ("users", User), ("moods", Mood), ("factors", Factor)):
                for row in data[table]:
                    obj = model(**{k: v if v is not None else ""
                                   for k, v in row.items()})
                    obj.full_clean()
                    obj.save(force_insert=True)
            for row in data["entries"]:
                row["comment"] = row["comment"] or ""
                obj = MoodEntry(**row)
                obj.full_clean()
                obj.save(force_insert=True)
            for link in data["entry_factors"]:
                MoodEntry.objects.get(pk=link["entry_id"]).factors.add(
                    Factor.objects.get(pk=link["factor_id"]))
        except (sqlite3.Error, ValueError) as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(self.style.SUCCESS(
            f"Перенесено записей: {MoodEntry.objects.count()}"))
