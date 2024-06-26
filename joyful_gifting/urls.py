"""
URL configuration for the Joyful Gifting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("apps.users.urls")),
    path("chats/", include("apps.chats.urls")),
    path("notifications/", include("apps.notices.urls")),
    path("notifications/", include("notifications.urls", namespace="notifications")),
    path("", include("apps.items.urls")),
    path("", include("apps.pages.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
