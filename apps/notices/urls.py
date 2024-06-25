from django.urls import path

from .views import check_notifications, open_notification


app_name = "notices"

urlpatterns = [
    path("check/", check_notifications, name="check"),
    path("<int:pk>/open/", open_notification, name="open-notification"),
]
