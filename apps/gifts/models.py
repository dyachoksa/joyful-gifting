import datetime as dt
import os
import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, pgettext_lazy, gettext
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail, SmartResize


def gift_image_location(_instance, filename):
    today = dt.date.today()

    basename, ext = os.path.splitext(filename)

    return "gifts/{}/{}{}".format(today.strftime("%Y/%m/%d"), uuid.uuid4(), ext)


class GiftStatus(models.TextChoices):
    NEW = "new", _("New")
    IN_REVIEW = "in_review", _("In Review")
    APPROVED = "approved", _("Approved")
    GIFTED = "gifted", _("Gifted")
    REJECTED = "rejected", _("Rejected")


class Gift(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gifted_by = models.ForeignKey(
        "users.User", on_delete=models.RESTRICT, related_name="gifts_by_me"
    )
    gifted_to = models.ForeignKey(
        "users.User",
        on_delete=models.RESTRICT,
        related_name="gifts_to_me",
        blank=True,
        null=True,
        db_default=None,
    )
    status = models.CharField(
        max_length=None,
        choices=GiftStatus.choices,
        default=GiftStatus.NEW,
        db_index=True,
        db_default=GiftStatus.NEW.value,
    )
    name = models.CharField(pgettext_lazy("gift model", "name"), max_length=None)
    description = models.TextField(
        _("description"),
        help_text=_(
            "The short description of the gift. It's condition and/or other helpful information."  # noqa: E501
        ),
    )
    image = models.ImageField(
        _("image"),
        max_length=None,
        upload_to=gift_image_location,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    gifted_at = models.DateTimeField(
        _("gifted at"), blank=True, null=True, default=None
    )

    image_thumbnail = ImageSpecField(
        source="image", processors=[Thumbnail(350, 300)], format="WEBP"
    )
    image_preview = ImageSpecField(
        source="image", processors=[SmartResize(640, 480)], format="WEBP"
    )

    class Meta:
        ordering = ("-created_at",)
        permissions = [
            ("can_manage_gift", _("Can manage gift")),
        ]
        verbose_name = _("gift")
        verbose_name_plural = _("gifts")

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Gift id={} name={}>".format(self.id, self.name)

    @property
    def is_gifted(self):
        return self.status == GiftStatus.GIFTED

    @property
    def is_new(self):
        return self.status == GiftStatus.NEW

    @property
    def in_review(self):
        return self.status == GiftStatus.IN_REVIEW

    @property
    def is_approved(self):
        return self.status == GiftStatus.APPROVED

    def get_absolute_url(self):
        return reverse("gifts:detail", kwargs={"pk": self.pk})

    def get_apply_url(self):
        return reverse("gifts:apply-for-gift", kwargs={"pk": self.pk})

    def get_approve_url(self):
        return reverse("gifts:approve-gift", kwargs={"pk": self.pk})

    def get_reject_url(self):
        return reverse("gifts:reject-gift", kwargs={"pk": self.pk})

    def is_owned_by(self, user):
        return self.gifted_by_id == user.id


class GiftImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gift = models.ForeignKey(
        Gift,
        on_delete=models.CASCADE,
        related_name="additional_images",
        verbose_name=_("gift"),
    )
    image = models.ImageField(
        _("image"), max_length=None, upload_to=gift_image_location
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("gift image")
        verbose_name_plural = _("gift images")

    def __str__(self):
        return self.image.name

    def __repr__(self):
        return "<GiftImage id={} gift={}>".format(self.id, self.gift_id)


class GiftApplicationStatus(models.TextChoices):
    NEW = "new", _("New")
    APPROVED = "approved", _("Approved")
    REJECTED = "rejected", _("Rejected")


class GiftApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE, verbose_name=_("gift"))
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        related_name="gift_applications",
    )
    status = models.CharField(
        _("status"),
        max_length=None,
        choices=GiftApplicationStatus.choices,
        default=GiftApplicationStatus.NEW,
        db_index=True,
        db_default=GiftApplicationStatus.NEW.value,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        ordering = ("created_at",)
        permissions = [
            ("can_manage_gift_application", _("Can manage gift application")),
        ]
        verbose_name = _("gift application")
        verbose_name_plural = _("gift applications")

    def __str__(self):
        return gettext("gift application")

    def __repr__(self):
        return "<GiftApplication id={} gift={} status={}>".format(
            self.id, self.gift_id, self.status
        )

    @property
    def is_active(self):
        return self.status == GiftApplicationStatus.NEW

    @property
    def is_new(self):
        return self.status == GiftApplicationStatus.NEW

    @property
    def is_approved(self):
        return self.status == GiftApplicationStatus.APPROVED

    @property
    def is_rejected(self):
        return self.status == GiftApplicationStatus.REJECTED

    def get_approve_url(self):
        return reverse("gifts:approve-gift-application", kwargs={"pk": self.pk})
