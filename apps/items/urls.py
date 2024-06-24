from django.urls import path

from .views import (
    GiftDetailView,
    GiftListView,
    apply_for_gift,
    approve_gift_application,
)

app_name = "items"

urlpatterns = [
    # Gifts
    path("gifts/<uuid:pk>/", GiftDetailView.as_view(), name="gift-detail"),
    path("gifts/<uuid:pk>/apply/", apply_for_gift, name="apply-for-gift"),
    path("gifts/", GiftListView.as_view(), name="gift-list"),
    # Gift's application
    path(
        "gift-application/<uuid:pk>/approve/",
        approve_gift_application,
        name="approve-gift-application",
    ),
]
