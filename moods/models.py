"""Справочники настроений и факторов влияния."""
from django.db import models


class Mood(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["name", "pk"]

    def __str__(self):
        return self.name


class Factor(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    class Meta:
        ordering = ["category", "name", "pk"]

    def __str__(self):
        return self.name
