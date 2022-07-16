# flake8: noqa

import socket

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

import astu_inventory

from .base import *

# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

EMAIL_HOST = socket.gethostbyname("smtp.gmail.com")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

SERVER_EMAIL = config("SERVER_EMAIL")

EMAIL_USE_TLS = True

EMAIL_HOST_USER = config("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

EMAIL_PORT = config("EMAIL_PORT", default=25, cast=int)

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

CSRF_COOKIE_SECURE = False

CSRF_COOKIE_HTTPONLY = False

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year

SECURE_HSTS_INCLUDE_SUBDOMAINS = False

SECURE_SSL_REDIRECT = False

SECURE_BROWSER_XSS_FILTER = False

SECURE_CONTENT_TYPE_NOSNIFF = False

# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = False

# ==============================================================================
# THIRD-PARTY APPS SETTINGS
# ==============================================================================

sentry_sdk.init(
    dsn=config("SENTRY_DSN", default=""),
    environment=ASTU_INVENTORY_ENVIRONMENT,
    release="simple@%s" % astu_inventory.__version__,
    integrations=[DjangoIntegration()],
)
