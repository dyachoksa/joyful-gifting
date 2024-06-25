from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET

from .models import Notification


@login_required
def check_notifications(request):
    return render(request, "notices/partials/notifications.html")


@require_GET
@login_required
def open_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.mark_as_read()

    target_url = notification.target_object_url()

    return redirect(target_url)
