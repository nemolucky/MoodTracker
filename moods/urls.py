from django.urls import path

from . import views

urlpatterns = [
    path("", views.moods, name="moods"),
    path("<int:mood_id>/", views.mood_detail, name="mood_detail"),
]
