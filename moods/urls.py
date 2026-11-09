from django.urls import path

from . import views

app_name = "moods"

urlpatterns = [
    path("by-slug/<slug:slug>/", views.mood_detail, name="detail_slug"),
    path("", views.moods, name="list"),
    path("<int:mood_id>/", views.mood_detail, name="detail"),
]
