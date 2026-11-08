"""CRUD дневника с проверкой данных на уровне модели."""
from django.db import transaction

from .models import MoodEntry


@transaction.atomic
def create_entry(*, factors=(), **fields):
    entry = MoodEntry(**fields)
    entry.full_clean()
    entry.save()
    entry.factors.set(factors)
    return entry


@transaction.atomic
def update_entry(entry_id, *, score, comment):
    entry = MoodEntry.objects.get(pk=entry_id)
    entry.score, entry.comment = score, comment
    entry.full_clean()
    entry.save(update_fields=["score", "comment"])
    return entry


def delete_entry(entry_id):
    return MoodEntry.objects.get(pk=entry_id).delete()
