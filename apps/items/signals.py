from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Gift


@receiver(pre_delete, sender=Gift, dispatch_uid="clean-gift-images")
def clean_gift_images(sender, instance: Gift, **kwargs):
    instance.image.delete(save=False)
