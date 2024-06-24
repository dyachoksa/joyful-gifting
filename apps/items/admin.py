from django.contrib import admin

from .models import Gift, GiftApplication, GiftImage


class GiftImageInline(admin.StackedInline):
    can_delete = True
    extra = 1
    max_num = 5
    model = GiftImage


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    inlines = [GiftImageInline]

    date_hierarchy = "created_at"

    list_display = ("name", "gifted_by", "status", "created_at", "gifted_at")
    list_select_related = ("gifted_by",)


@admin.register(GiftApplication)
class GiftApplicationAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"

    list_display = ("gift", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    list_select_related = ("gift", "user")
