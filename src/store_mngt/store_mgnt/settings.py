"""
Django settings for store_mgnt project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from dj_database_url import parse as db_url
from django.contrib.messages import constants as messages
from django.urls import reverse_lazy
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.admindocs",
    "django.contrib.flatpages",

    # Third Party
    'widget_tweaks',
    'ckeditor',
    "django_social_share",
    "django_filters",

    # Local
    'auser',
    # 'pages',  # dont forget after everything is okay
    'item',
]  

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
 
ROOT_URLCONF = 'store_mgnt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'store_mgnt.wsgi.application'

  
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': config (
        "DATABASE_URL", default="sqlite:///" / BASE_DIR / "db.sqlite3", cast = db_url
    )
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# The absolute path to the directory where 'collectstatic' will collect static files.
STATIC_ROOT = BASE_DIR / "assets"

# This setting defines the additional locations the staticfiles app will traverse
STATICFILES_DIRS = (BASE_DIR / "static",)

# URL that handles the media served from MEDIA_ROOT,
MEDIA_URL = "/contents/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = BASE_DIR / "uploads"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# The model to use to represent a current User.
AUTH_USER_MODEL = "auser.User"

SITE_ID = 1

# The URL or named URL pattern where requests are redirected for login
LOGIN_URL = reverse_lazy("auser:login")

# The URL or named URL pattern where requests are redirected after login
# LOGIN_REDIRECT_URL = reverse_lazy("pages:dashboard")

# The URL or named URL pattern where requests are redirected after logout
# LOGOUT_REDIRECT_URL = LOGIN_URL

# A list of authentication backend classes to use when attempting to authenticate a user.
# AUTHENTICATION_BACKENDS = [
#     "auser.backends.EmailBackend",
#     "django.contrib.auth.backends.ModelBackend",
# ]

# A mapping of message level to message tag,
MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

FILTERS_VERBOSE_LOOKUPS = {
    "exact": "",
    "iexact": "",
    "contains": "",
    "icontains": "",
}

# An app which provides customization of the comments framework
COMMENTS_APP = "comment"

GEOIP_PATH = BASE_DIR / "tracking/geoip"
if DEBUG:
    ALLOWED_HOSTS.append("*")

    # The backend to use for sending emails.
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

    # The directory used by the file email backend to store output files.
    EMAIL_FILE_PATH = BASE_DIR / "emails"