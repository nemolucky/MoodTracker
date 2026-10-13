from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("", views.entries, name="list"),
    path("<int:entry_id>/", views.entry_detail, name="detail"),
]
