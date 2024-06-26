import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(
        "users.User", related_name="chats", blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)
        verbose_name = _("chat")
        verbose_name_plural = _("chats")

    def __str__(self):
        return gettext("chat")

    def get_absolute_url(self):
        return reverse("chats:detail", kwargs={"pk": self.pk})

    def get_chat_messages(self):
        return self.messages.select_related("sender").order_by("created_at")


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="messages", db_index=True
    )
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="+",
        blank=True,
        null=True,
        verbose_name=_("message sender"),
        db_index=True,
        db_comment="Can be null for system messages",
    )
    message = models.TextField(_("message"), blank=False, null=False)
    is_read = models.BooleanField(_("is read"), default=False)
    extra_data = models.JSONField(_("extra data"), default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("message")
        verbose_name_plural = _("messages")

    def __str__(self):
        return gettext("chat message")
