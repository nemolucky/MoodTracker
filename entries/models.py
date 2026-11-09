"""Модели дневника; консольные модели ПР3 сохранены отдельно."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, default="")

    def __str__(self):
        return self.name


class MoodEntry(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="entries")
    mood = models.ForeignKey(
        "moods.Mood", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="entries")
    factors = models.ManyToManyField(
        "moods.Factor", blank=True, related_name="entries")
    entry_date = models.DateField(db_index=True)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-entry_date", "-pk"]
        constraints = [models.CheckConstraint(
            condition=models.Q(score__gte=0, score__lte=10),
            name="entry_score_0_10")]

    def __str__(self):
        return f"{self.entry_date}: {self.score}/10"

    @property
    def status(self):
        if self.score >= 7:
            return "Хороший день"
        if self.score >= 4:
            return "Нейтральный день"
        return "Плохой день"
