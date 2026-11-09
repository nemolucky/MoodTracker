"""Регрессия ORM, импорта и пользовательских сценариев ПР9."""
import hashlib
import sqlite3
from io import StringIO

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.test import TestCase

from entries.models import MoodEntry, User
from entries.services import create_entry, delete_entry, update_entry
from moods.models import Factor, Mood


class ORMTests(TestCase):
    def test_import_matches_source(self):
        source = settings.BASE_DIR / "data" / "moodtracker.sqlite"
        before = hashlib.sha256(source.read_bytes()).digest()
        with sqlite3.connect(source) as conn:
            for table, model in (("users", User), ("moods", Mood),
                                 ("factors", Factor), ("entries", MoodEntry)):
                conn.row_factory = sqlite3.Row
                for row in conn.execute(f"SELECT * FROM {table}"):
                    obj = model.objects.get(pk=row["id"])
                    for field, value in dict(row).items():
                        actual = getattr(obj, field)
                        if field == "entry_date":
                            actual = actual.isoformat()
                        self.assertEqual(actual, value or (
                            "" if field in ("email", "comment",
                                            "description") else value))
            expected = set(conn.execute(
                "SELECT entry_id, factor_id FROM entry_factors"))
            actual = set(MoodEntry.factors.through.objects.values_list(
                "moodentry_id", "factor_id"))
            self.assertEqual({tuple(r) for r in expected}, actual)
        self.assertEqual(before, hashlib.sha256(source.read_bytes()).digest())

    def test_repeat_import_is_rejected(self):
        count = MoodEntry.objects.count()
        with self.assertRaises(CommandError):
            call_command("import_pr7", stdout=StringIO())
        self.assertEqual(count, MoodEntry.objects.count())

    def test_crud_and_validation(self):
        entry = create_entry(user=User.objects.first(),
                             entry_date="2026-11-08",
                             score=7, factors=list(Factor.objects.all()[:1]))
        self.assertEqual(entry.user.entries.get(pk=entry.pk), entry)
        self.assertEqual(entry.factors.count(), 1)
        update_entry(entry.pk, score=2, comment="Обновлено")
        entry.refresh_from_db()
        self.assertEqual(entry.status, "Плохой день")
        with self.assertRaises(ValidationError):
            update_entry(entry.pk, score=11, comment="Ошибка")
        delete_entry(entry.pk)
        self.assertFalse(MoodEntry.objects.filter(pk=entry.pk).exists())

    def test_constraints_and_delete_policies(self):
        entry = MoodEntry.objects.first()
        with self.assertRaises(ProtectedError):
            entry.user.delete()
        with self.assertRaises(IntegrityError), transaction.atomic():
            MoodEntry.objects.filter(pk=entry.pk).update(score=11)
        mood = entry.mood
        mood.delete()
        entry.refresh_from_db()
        self.assertIsNone(entry.mood)
        factor = Factor.objects.first()
        factor.delete()
        self.assertTrue(MoodEntry.objects.filter(pk=entry.pk).exists())

    def test_filters_search_sort_and_pagination(self):
        for score in range(8):
            create_entry(user=User.objects.first(), entry_date="2026-11-08",
                         score=score, comment="unique needle")
        response = self.client.get("/entries/", {
            "q": "unique needle", "date": "2026-11-08",
            "min_score": 2, "sort": "score", "page": 2})
        self.assertEqual(response.status_code, 200)
        page = response.context["page_obj"]
        self.assertEqual(page.paginator.count, 6)
        self.assertEqual([e.score for e in page], [4, 3, 2])
        self.assertContains(response, "min_score=2")
        self.assertContains(response, "sort=score")
        for params in ({"date": "bad"}, {"mood": "99999"},
                       {"min_score": "11"}, {"sort": "injection"}):
            response = self.client.get("/entries/", params)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["page_obj"].paginator.count, 0)
        for page in ("bad", "99999", "-1"):
            self.assertEqual(self.client.get(
                "/entries/", {"page": page}).status_code, 200)

    def test_related_search_and_unused_moods(self):
        entry = MoodEntry.objects.get(pk=1)
        response = self.client.get("/entries/", {"q": entry.user.name})
        self.assertGreater(response.context["page_obj"].paginator.count, 0)
        response = self.client.get("/entries/", {"mood": entry.mood_id})
        self.assertTrue(all(e.mood_id == entry.mood_id
                            for e in response.context["entries"]))
        response = self.client.get("/moods/", {"q": entry.mood.name})
        self.assertIn(entry.mood, response.context["moods"])
        response = self.client.get("/entries/search/", {"date": "bad"})
        self.assertTrue(response.context["errors"])

    def test_statistics_includes_empty_mood(self):
        mood = Mood.objects.create(name="Без записей")
        response = self.client.get("/entries/statistics/")
        stat = next(row for row in response.context["mood_stats"]
                    if row.pk == mood.pk)
        self.assertEqual(stat.entries_count, 0)
        self.assertIsNone(stat.avg_score)
        self.assertEqual(response.context["overall"]["total_entries"],
                         MoodEntry.objects.count())

    def test_detail_query_count_and_empty_factors(self):
        entry = create_entry(user=User.objects.first(),
                             entry_date="2026-11-08",
                             score=0)
        with self.assertNumQueries(2):
            response = self.client.get(f"/entries/{entry.pk}/")
        self.assertContains(response, "Не указаны")
        self.assertContains(response, "Плохой день")
