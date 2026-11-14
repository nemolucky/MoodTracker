"""HTTP-проверки форм ПР11 на изолированной базе."""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from entries.models import MoodEntry, User
from moods.models import Factor


class EntryFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.editor = get_user_model().objects.create_superuser(
            "forms-editor", "", "test-only-password")

    def setUp(self):
        self.client.force_login(self.editor)
        self.data = {"user": User.objects.first().pk,
                     "entry_date": timezone.localdate().isoformat(),
                     "score": 8, "comment": "Новая запись"}

    def test_create_get_post_redirect_and_m2m(self):
        url = reverse("entries:create")
        count = MoodEntry.objects.count()
        response = self.client.get(url)
        self.assertFalse(response.context["form"].is_bound)
        self.assertEqual(MoodEntry.objects.count(), count)
        factor = Factor.objects.first()
        self.data["factors"] = [factor.pk]
        response = self.client.post(url, self.data)
        entry = MoodEntry.objects.latest("pk")
        self.assertRedirects(response, reverse(
            "entries:detail", args=[entry.pk]))
        self.assertEqual(entry.factors.get(), factor)
        self.assertEqual(MoodEntry.objects.count(), count + 1)
        self.client.get(response.url)
        self.assertEqual(MoodEntry.objects.count(), count + 1)

    def test_invalid_data_retained_without_save(self):
        count = MoodEntry.objects.count()
        for patch, field in (({"score": 11}, "score"),
                             ({"entry_date": "bad"}, "entry_date"),
                             ({"user": 99999}, "user"),
                             ({"score": 1, "comment": " "}, "__all__"),
                             ({"entry_date": (timezone.localdate() +
                              timedelta(days=1)).isoformat()}, "entry_date")):
            response = self.client.post(reverse("entries:create"),
                                        {**self.data, **patch})
            self.assertEqual(response.status_code, 200)
            form = response.context["form"]
            self.assertTrue(form.is_bound)
            self.assertIn(field, form.errors)
            self.assertEqual(MoodEntry.objects.count(), count)

    def test_edit_instance_and_archive(self):
        entry = MoodEntry.objects.get(pk=1)
        url = reverse("entries:edit", args=[entry.pk])
        self.assertEqual(self.client.get(url).context["form"].instance, entry)
        data = {**self.data, "entry_date": entry.entry_date.isoformat()}
        count = MoodEntry.objects.count()
        self.assertEqual(self.client.post(url, data).status_code, 302)
        self.assertEqual(MoodEntry.objects.count(), count)
        entry.refresh_from_db()
        self.assertEqual(entry.comment, data["comment"])
        archive = reverse("entries:archive", args=[entry.pk])
        self.assertEqual(self.client.get(archive).status_code, 405)
        entry.refresh_from_db()
        self.assertEqual(entry.publication_status, MoodEntry.Status.PUBLISHED)
        self.assertEqual(self.client.post(archive).status_code, 302)
        entry.refresh_from_db()
        self.assertEqual(entry.publication_status, MoodEntry.Status.ARCHIVED)
        self.assertEqual(MoodEntry.objects.count(), count)
        self.assertEqual(self.client.get(reverse(
            "entries:detail", args=[entry.pk])).status_code, 404)
        self.assertEqual(self.client.post(archive).status_code, 302)

    def test_permissions_missing_objects_and_csrf(self):
        for name in ("edit", "archive"):
            url = reverse(f"entries:{name}", args=[99999])
            self.assertEqual(self.client.post(url, self.data).status_code, 404)
        self.client.logout()
        self.assertEqual(self.client.post(reverse(
            "entries:create"), self.data).status_code, 403)
        ordinary = get_user_model().objects.create_user("forms-ordinary")
        self.client.force_login(ordinary)
        self.assertEqual(self.client.get(reverse(
            "entries:create")).status_code, 403)
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.editor)
        url = reverse("entries:create")
        self.assertEqual(csrf_client.post(url, self.data).status_code, 403)
        response = csrf_client.get(url)
        self.assertContains(response, "csrfmiddlewaretoken")
        token = csrf_client.cookies["csrftoken"].value
        self.assertEqual(csrf_client.post(url, {
            **self.data, "csrfmiddlewaretoken": token}).status_code, 302)
