"""
Django settings for astu_inventory project.

Generated by 'django-admin startproject' using Django 3.2.4.
"""
from pathlib import Path

from django.contrib.messages import constants as messages
from django.urls import reverse_lazy

import dj_database_url
from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# CORE SETTINGS
# ==============================================================================

SECRET_KEY = config("SECRET_KEY", default="django-insecure$astu_inventory.settings.local")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "astu_inventory.urls"

WSGI_APPLICATION = "astu_inventory.wsgi.application"

INTERNAL_IPS = ["127.0.0.1"]

# ==============================================================================
# APPLICATION DEFINATIONS
# ==============================================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "widget_tweaks",
    "smart_selects",
    "django_summernote",
    # Local apps
    "astu_inventory.apps.auser",
    "astu_inventory.apps.inventory",
    "astu_inventory.apps.core",
]

# ==============================================================================
# MIDDLEWARE SETTINGS
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==============================================================================
# TEMPLATES SETTINGS
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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


# ==============================================================================
# DATABASES SETTINGS
# ==============================================================================

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default="sqlite:///db.sqlite3"),
        conn_max_age=600,
    )
}

# ==============================================================================
# AUTHENTICATION AND AUTHORIZATION SETTINGS
# ==============================================================================

AUTH_USER_MODEL = "auser.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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

# The URL or named URL pattern where requests are redirected for login
LOGIN_URL = reverse_lazy("auser:login")

# The URL or named URL pattern where requests are redirected after login
LOGIN_REDIRECT_URL = reverse_lazy("core:dashboard")

# The URL or named URL pattern where requests are redirected after logout
LOGOUT_REDIRECT_URL = LOGIN_URL

# ==============================================================================
# I18N AND L10N SETTINGS
# ==============================================================================

LANGUAGE_CODE = config("LANGUAGE_CODE", default="en-us")

TIME_ZONE = config("TIME_ZONE", default="UTC")

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]

# ==============================================================================
# STATIC FILES SETTINGS
# ==============================================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR.parent.parent / "asset"

STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# ==============================================================================
# MEDIA FILES SETTINGS
# ==============================================================================

MEDIA_URL = "/uploads/"

MEDIA_ROOT = BASE_DIR.parent.parent / "uploads"

# ==============================================================================
# MESSAGE CONFIGURATION
# ==============================================================================

MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# ==============================================================================
# THIRD-PARTY SETTINGS
# ==============================================================================

# django smart select

USE_DJANGO_JQUERY = True

# Summernote

SUMMERNOTE_CONFIG = {

    'iframe': False,
    'summernote': {
        # Change editor size
        'width': '100%',
        'height': '480',
    },
}

# ==============================================================================
# FIRST-PARTY SETTINGS
# ==============================================================================
ASTU_INVENTORY_ENVIRONMENT = config("ASTU_INVENTORY_ENVIRONMENT", default="local")
