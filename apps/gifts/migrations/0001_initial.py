# Generated by Django 5.0.6 on 2024-06-22 12:37

import apps.gifts.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Gift",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "New"),
                            ("in_review", "In Review"),
                            ("approved", "Approved"),
                            ("gifted", "Gifted"),
                            ("rejected", "Rejected"),
                        ],
                        db_default="new",
                        db_index=True,
                        default="new",
                    ),
                ),
                ("name", models.CharField(verbose_name="name")),
                (
                    "description",
                    models.TextField(
                        help_text="The short description of the gift. It's condition and/or other helpful information.",
                        verbose_name="description",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=apps.gifts.models.gift_image_location,
                        verbose_name="image",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "gifted_at",
                    models.DateTimeField(
                        blank=True, default=None, null=True, verbose_name="gifted at"
                    ),
                ),
                (
                    "gifted_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="gifts_by_me",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "gifted_to",
                    models.ForeignKey(
                        blank=True,
                        db_default=None,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="gifts_to_me",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "gift",
                "verbose_name_plural": "gifts",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="GiftApplication",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "New"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                        ],
                        db_default="new",
                        db_index=True,
                        default="new",
                        verbose_name="status",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "gift",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="gifts.gift",
                        verbose_name="gift",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gift_applications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "gift application",
                "verbose_name_plural": "gift applications",
                "ordering": ("created_at",),
            },
        ),
        migrations.CreateModel(
            name="GiftImage",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=apps.gifts.models.gift_image_location,
                        verbose_name="image",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "gift",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="additional_images",
                        to="gifts.gift",
                        verbose_name="gift",
                    ),
                ),
            ],
            options={
                "verbose_name": "gift image",
                "verbose_name_plural": "gift images",
            },
        ),
    ]
