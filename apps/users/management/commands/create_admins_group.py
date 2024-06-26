from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from apps.gifts.models import Gift, GiftApplication


class Command(BaseCommand):
    help = "Creates admin group"

    def handle(self, *args, **options):
        try:
            Group.objects.get(name=settings.ADMINS_GROUP_NAME)
            self.stdout.write("Admin group already exists")
        except Group.DoesNotExist:
            admins = Group.objects.create(name=settings.ADMINS_GROUP_NAME)

            gift_content_type = ContentType.objects.get_for_model(Gift)
            gift_manage_permission = Permission.objects.get(
                codename="can_manage_gift", content_type=gift_content_type
            )

            application_content_type = ContentType.objects.get_for_model(
                GiftApplication
            )
            application_manage_permission = Permission.objects.get(
                codename="can_manage_gift_application",
                content_type=application_content_type,
            )

            admins.permissions.set(
                [gift_manage_permission, application_manage_permission]
            )

            self.stdout.write(self.style.SUCCESS("Created admin group"))
