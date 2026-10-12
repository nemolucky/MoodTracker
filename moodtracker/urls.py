from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("entries/", include("entries.urls")),
    path("moods/", include("moods.urls")),
]

handler404 = "homepage.views.page_not_found"
