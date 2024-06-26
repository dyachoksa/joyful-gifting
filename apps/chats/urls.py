from django.urls import path

from .views import ChatListView, chat_details

app_name = "chats"

urlpatterns = [
    path("<uuid:pk>/", chat_details, name="detail"),
    path("", ChatListView.as_view(), name="list"),
]
