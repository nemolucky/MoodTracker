"""Права, формы админки, статусы и сохранение сценариев ПР9."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from entries.models import MoodEntry
from moods.models import Mood


class AdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser(
            "test-admin", "test@example.com", "test-only-password")

    def test_access_control(self):
        url = reverse("admin:entries_moodentry_changelist")
        self.assertEqual(self.client.get(url).status_code, 302)
        user = get_user_model().objects.create_user("regular")
        self.client.force_login(user)
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(self.admin_user)
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_admin_lists_and_inlines(self):
        self.client.force_login(self.admin_user)
        for model in ("entries_user", "entries_moodentry",
                      "moods_mood", "moods_factor"):
            self.assertEqual(self.client.get(reverse(
                f"admin:{model}_changelist")).status_code, 200)
        entry = MoodEntry.objects.get(pk=1)
        for model, obj in (("entries_user", entry.user),
                           ("moods_mood", entry.mood)):
            response = self.client.get(reverse(
                f"admin:{model}_change", args=[obj.pk]))
            self.assertContains(response, "entries-0-entry_date")
        response = self.client.get(reverse(
            "admin:entries_moodentry_changelist"), {"q": entry.user.name})
        self.assertContains(response, entry.user.name)
        response = self.client.get(reverse(
            "admin:entries_moodentry_changelist"),
            {"publication_status__exact": "draft"})
        self.assertEqual(response.context["cl"].result_count, 0)

    def test_admin_save_status_and_validation(self):
        self.client.force_login(self.admin_user)
        entry = MoodEntry.objects.get(pk=1)
        url = reverse("admin:entries_moodentry_change", args=[entry.pk])
        data = {"user": entry.user_id, "mood": entry.mood_id,
                "entry_date": entry.entry_date.isoformat(),
                "score": entry.score, "comment": entry.comment,
                "publication_status": "archived", "_save": "Сохранить"}
        self.assertEqual(self.client.post(url, data).status_code, 302)
        entry.refresh_from_db()
        self.assertEqual(entry.publication_status, MoodEntry.Status.ARCHIVED)
        self.assertEqual(self.client.get(
            reverse("entries:detail", args=[entry.pk])).status_code, 404)
        data["score"] = 11
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("score", response.context["adminform"].form.errors)

    def test_statuses_affect_views_and_statistics(self):
        entry = MoodEntry.objects.get(pk=1)
        original = MoodEntry.objects.published().count()
        for status in (MoodEntry.Status.DRAFT, MoodEntry.Status.ARCHIVED):
            entry.publication_status = status
            entry.save()
            response = self.client.get(reverse("entries:list"))
            self.assertEqual(response.context["page_obj"].paginator.count,
                             original - 1)
            response = self.client.get(reverse("entries:statistics"))
            self.assertEqual(response.context["overall"]["total_entries"],
                             original - 1)
            counts = {row["publication_status"]: row["entries_count"]
                      for row in response.context["status_stats"]}
            self.assertEqual(counts[status], 1)
            response = self.client.get(reverse("entries:search"), {
                "date": entry.entry_date.isoformat()})
            self.assertNotIn(entry, response.context["entries"])
            response = self.client.get(entry.mood.get_absolute_url())
            self.assertNotIn(entry, response.context["related_entries"])
        entry.publication_status = MoodEntry.Status.PUBLISHED
        entry.save()
        self.assertEqual(MoodEntry.objects.published().count(), original)

    def test_slug_and_context(self):
        mood = Mood.objects.first()
        self.assertEqual(self.client.get(
            mood.get_absolute_url()).status_code, 200)
        self.assertEqual(self.client.get(reverse(
            "moods:detail", args=[mood.pk])).status_code, 200)
        self.assertEqual(self.client.get(
            "/moods/by-slug/missing/").status_code, 404)
        self.assertNotEqual(mood.slug, Mood.objects.create(
            name="Новое настроение").slug)
        response = self.client.get("/")
        self.assertEqual(response.context["site_name"], "Mood Tracker")

    def test_related_query_count_is_constant(self):
        entry = MoodEntry.objects.get(pk=1)
        with self.assertNumQueries(1):
            rows = list(MoodEntry.objects.published().with_relations())
            for row in rows:
                str(row.user)
                str(row.mood)
        with self.assertNumQueries(2):
            response = self.client.get(reverse(
                "entries:detail", args=[entry.pk]))
        self.assertContains(response, entry.mood.name)
