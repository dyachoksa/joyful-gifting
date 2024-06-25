from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from notifications.base.models import AbstractNotification


class Notification(AbstractNotification):
    class Meta(AbstractNotification.Meta):
        abstract = False
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")

    def get_absolute_url(self):
        return reverse("notices:open-notification", kwargs={"pk": self.pk})

    def target_object_url(self):
        url = reverse("items:gift-list")

        if self.target and hasattr(self.target, "get_absolute_url"):
            url = self.target.get_absolute_url()

        return url
