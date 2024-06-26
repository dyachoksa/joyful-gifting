from django.urls import path

from .views import index, about

app_name = "pages"

urlpatterns = [
    path("about-us/", about, name="about"),
    path("", index, name="index"),
]
