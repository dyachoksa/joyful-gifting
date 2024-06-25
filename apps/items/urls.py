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

app_name = "items"

urlpatterns = [
    # Gifts
    path("gifts/create/", GiftCreateView.as_view(), name="gift-create"),
    path("gifts/<uuid:pk>/", GiftDetailView.as_view(), name="gift-detail"),
    path("gifts/<uuid:pk>/approve/", approve_gift, name="approve-gift"),
    path("gifts/<uuid:pk>/reject/", reject_gift, name="reject-gift"),
    path("gifts/<uuid:pk>/apply/", apply_for_gift, name="apply-for-gift"),
    path("gifts/", GiftListView.as_view(), name="gift-list"),
    # Gift's application
    path(
        "gift-application/<uuid:pk>/approve/",
        approve_gift_application,
        name="approve-gift-application",
    ),
]
