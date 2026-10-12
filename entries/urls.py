from django.urls import path

from . import views

urlpatterns = [
    path("", views.entries, name="entries"),
    path("<int:entry_id>/", views.entry_detail, name="entry_detail"),
]
