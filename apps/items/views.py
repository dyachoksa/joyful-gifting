from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django_htmx.http import HttpResponseClientRedirect
from notifications.signals import notify

from .models import Gift, GiftStatus, GiftApplication
from ..notices.models import Notification


class GiftListView(LoginRequiredMixin, ListView):
    model = Gift
    context_object_name = "gifts"
    paginate_by = 12

    def get_queryset(self):
        return Gift.objects.filter(status=GiftStatus.APPROVED)


class GiftDetailView(LoginRequiredMixin, DetailView):
    model = Gift
    context_object_name = "gift"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["requests"] = GiftApplication.objects.filter(gift=self.object).order_by(
            "created_at"
        )

        return context


@require_POST
@login_required
def apply_for_gift(request, pk):
    gift = get_object_or_404(Gift, pk=pk)

    try:
        GiftApplication.objects.get(gift=gift, user=request.user)

        return (
            HttpResponseClientRedirect(gift.get_absolute_url())
            if request.htmx
            else redirect("items:gift-detail", pk=gift.pk)
        )
    except GiftApplication.DoesNotExist:
        application = GiftApplication.objects.create(gift=gift, user=request.user)

        admins_group = Group.objects.get(name=settings.ADMINS_GROUP_NAME)
        notify.send(
            request.user,
            recipient=admins_group,
            verb="applied",
            action_object=application,
            target=gift,
        )

    context = {"gift": gift}

    if request.htmx:
        return render(request, "items/partials/want_button.html", context=context)

    return redirect("items:gift-detail", pk=gift.pk)


@require_POST
@permission_required("items.can_manage_gift_application")
@transaction.atomic
def approve_gift_application(request, pk):
    application: GiftApplication = get_object_or_404(
        GiftApplication.objects.select_related("gift", "user"), pk=pk
    )

    if not application.is_new:
        raise RuntimeError("Gift application already approved/rejected")

    GiftApplication.objects.exclude(pk=application.pk).filter(
        gift=application.gift
    ).update(status=GiftStatus.REJECTED)

    application.status = GiftStatus.APPROVED
    # todo: add updated_by
    application.save()

    application.gift.status = GiftStatus.GIFTED
    application.gift.gifted_at = timezone.now()
    application.gift.gifted_to = application.user
    application.gift.save()

    notify.send(
        request.user,
        recipient=application.user,
        verb=_("approved"),
        action_object=application,
        target=application.gift,
        description=_("Your gift application has been approved"),
        level=Notification.LEVELS.success,
    )

    if not request.htmx:
        messages.success(request, "Gift application approved")
        return redirect("items:gift-detail", pk=application.gift.pk)

    context = {
        "gift": application.gift,
        "requests": GiftApplication.objects.filter(gift=application.gift).order_by(
            "created_at"
        ),
    }

    # todo: add toast notification trigger
    return render(request, "items/partials/gift_requests.html", context=context)
