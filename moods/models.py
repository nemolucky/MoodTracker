"""Справочники настроений и факторов влияния."""
from django.db import models
from django.urls import reverse
from uuid import uuid4


def mood_slug():
    return uuid4().hex


class Mood(models.Model):
    slug = models.SlugField("Адрес", unique=True, default=mood_slug)
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True, default="")

    class Meta:
        verbose_name = "Настроение"
        verbose_name_plural = "Настроения"
        ordering = ["name", "pk"]

    def get_absolute_url(self):
        return reverse("moods:detail_slug", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Factor(models.Model):
    name = models.CharField("Название", max_length=100)
    category = models.CharField("Категория", max_length=100)

    class Meta:
        verbose_name = "Фактор влияния"
        verbose_name_plural = "Факторы влияния"
        ordering = ["category", "name", "pk"]

    def __str__(self):
        return self.name
