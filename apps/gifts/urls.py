from django.urls import path

from .views import (
    GiftDetailView,
    GiftListView,
    GiftCreateView,
    approve_gift,
    reject_gift,
    apply_for_gift,
    approve_gift_application,
)

app_name = "gifts"

urlpatterns = [
    # Gift's application
    path(
        "applications/<uuid:pk>/approve/",
        approve_gift_application,
        name="approve-gift-application",
    ),
    # Gifts
    path("create/", GiftCreateView.as_view(), name="create"),
    path("<uuid:pk>/", GiftDetailView.as_view(), name="detail"),
    path("<uuid:pk>/approve/", approve_gift, name="approve-gift"),
    path("<uuid:pk>/reject/", reject_gift, name="reject-gift"),
    path("<uuid:pk>/apply/", apply_for_gift, name="apply-for-gift"),
    path("", GiftListView.as_view(), name="list"),
]
