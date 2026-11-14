"""Модели дневника; консольные модели ПР3 сохранены отдельно."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class EntryQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publication_status=MoodEntry.Status.PUBLISHED)

    def on_date(self, date):
        return self.filter(entry_date=date)

    def with_relations(self):
        return self.select_related("user", "mood")


class User(models.Model):
    name = models.CharField("Имя", max_length=100)
    email = models.EmailField("Почта", blank=True, default="")

    class Meta:
        verbose_name = "Владелец дневника"
        verbose_name_plural = "Владельцы дневников"

    def __str__(self):
        return self.name


class MoodEntry(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PUBLISHED = "published", "Опубликована"
        ARCHIVED = "archived", "В архиве"

    publication_status = models.CharField(
        "Статус публикации", max_length=12, choices=Status.choices,
        default=Status.PUBLISHED, db_index=True)
    objects = EntryQuerySet.as_manager()

    user = models.ForeignKey(
        User, verbose_name="Владелец", on_delete=models.PROTECT,
        related_name="entries")
    mood = models.ForeignKey(
        "moods.Mood", verbose_name="Настроение", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="entries")
    factors = models.ManyToManyField(
        "moods.Factor", verbose_name="Факторы", blank=True,
        related_name="entries")
    entry_date = models.DateField("Дата", db_index=True)
    score = models.PositiveSmallIntegerField(
        "Оценка",
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField("Комментарий", blank=True, default="")

    class Meta:
        verbose_name = "Запись настроения"
        verbose_name_plural = "Записи настроения"
        ordering = ["-entry_date", "-pk"]
        constraints = [models.CheckConstraint(
            condition=models.Q(score__gte=0, score__lte=10),
            name="entry_score_0_10")]

    def __str__(self):
        return f"{self.entry_date}: {self.score}/10"

    def archive(self):
        self.publication_status = self.Status.ARCHIVED
        self.save(update_fields=["publication_status"])

    @property
    def status(self):
        if self.score >= 7:
            return "Хороший день"
        if self.score >= 4:
            return "Нейтральный день"
        return "Плохой день"
