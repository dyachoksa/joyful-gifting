from django import template

from apps.items.models import GiftApplication

register = template.Library()


@register.filter
def gifted_by(gift, user):
    """Checks if given gift is gifted/created by given user."""
    return gift.is_owned_by(user)


@register.filter
def has_active_application_by(gift, user):
    """Checks if given gift has active (new) application by given user."""
    try:
        application = GiftApplication.objects.get(gift=gift, user=user)
        return application.is_active
    except GiftApplication.DoesNotExist:
        return False


@register.simple_tag
def gift_application_for(gift, _as, user) -> GiftApplication | None:
    """Returns GiftApplication object for given gift and user."""
    return GiftApplication.objects.filter(gift=gift, user=user).first()
