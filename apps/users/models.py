import uuid

from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        if not username:
            username = email.strip().lower().split("@")[0]

        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(
        self, username=None, email=None, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("The given email must be set")

        if not username:
            username = email.strip().lower().split("@")[0]

        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_("username"), max_length=150, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def __repr__(self):
        return "<User id={} email={} is_active={} date_joined={}>".format(
            self.id, self.email, self.is_active, self.date_joined
        )

    def get_short_name(self):
        return self.first_name or self.email
