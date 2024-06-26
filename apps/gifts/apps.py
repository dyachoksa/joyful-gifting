from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GiftsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.gifts"
    verbose_name = _("Gifts")

    def ready(self):
        from . import signals  # noqa: F401
