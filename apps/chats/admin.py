from django.contrib import admin

from .models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"

    list_display = ("id", "created_at", "updated_at")
