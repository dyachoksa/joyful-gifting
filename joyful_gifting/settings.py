"""
Django settings for the Joyful Gifting project.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(BASE_DIR / ".env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "debug_toolbar",
    "django_bootstrap5",
    "django_extensions",
    "django_htmx",
    "notifications",
    # Project apps
    "apps.items",
    "apps.notices",
    "apps.pages",
    "apps.users",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "joyful_gifting.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "joyful_gifting" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "joyful_gifting.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": env.db_url(),
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_AUTHENTICATION_METHOD = "username_email"

ACCOUNT_EMAIL_REQUIRED = True

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"

ADMINS_GROUP_NAME = "Адміністратори"


# Email settings

email_env = env.email_url()

EMAIL_BACKEND = email_env.get(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = email_env.get("EMAIL_HOST", "localhost")

EMAIL_PORT = email_env.get("EMAIL_PORT", 1025)

EMAIL_HOST_USER = email_env.get("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = email_env.get("EMAIL_HOST_PASSWORD")

EMAIL_USE_TLS = email_env.get("EMAIL_USE_TLS", False)

EMAIL_USE_SSL = email_env.get("EMAIL_USE_SSL", False)


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "uk-ua"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / "joyful_gifting" / "locale",
]

LANGUAGES = [
    ("uk", _("Ukrainian")),
    ("en", _("English")),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "public" / "static"

STATICFILES_DIRS = [
    BASE_DIR / "joyful_gifting" / "static",
]

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "public" / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Notifications & messages

NOTIFICATIONS_NOTIFICATION_MODEL = "notices.Notification"

DJANGO_NOTIFICATIONS_CONFIG = {
    "USE_JSONFIELD": True,
}


# Other settings

INTERNAL_IPS = ["127.0.0.1"]
