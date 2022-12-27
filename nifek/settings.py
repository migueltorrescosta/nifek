"""
Django settings for nifek project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-urdm6)cbdt&7%)=vy6p)988h04n4zgww87d)9wr-&f-9j=8yh9"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0", "nifek.com", "https://nifek.com"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "magiclink",
    "accounts",
    "thes",
    "hold",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "magiclink.backends.MagicLinkBackend",
    "django.contrib.auth.backends.ModelBackend",
]

ROOT_URLCONF = "nifek.urls"

TEMPLATES_DIRS = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIRS],
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


WSGI_APPLICATION = "nifek.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_NAME"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

LOGIN_URL = "magiclink:login"
MAGICLINK_LOGIN_TEMPLATE_NAME = "magiclink/login.html"
MAGICLINK_LOGIN_SENT_TEMPLATE_NAME = "magiclink/login_sent.html"
MAGICLINK_LOGIN_FAILED_TEMPLATE_NAME = "magiclink/login_failed.html"
MAGICLINK_REQUIRE_SIGNUP = False
MAGICLINK_LOGIN_SENT_REDIRECT = "magiclink:login_sent"

# Ensure the branding of the login email is correct. This setting is not needed
# if you override the `login_email.html` template
MAGICLINK_EMAIL_STYLES = {
    "logo_url": "",
    "background-colour": "#ffffff",
    "main-text-color": "#000000",
    "button-background-color": "#0078be",
    "button-text-color": "#ffffff",
}

MAGICLINK_AUTH_TIMEOUT = 24 * 60 * 60 * 7  # 1 week
MAGICLINK_IGNORE_EMAIL_CASE = True
MAGICLINK_EMAIL_AS_USERNAME = True
MAGICLINK_ALLOW_SUPERUSER_LOGIN = True
MAGICLINK_ALLOW_STAFF_LOGIN = True
# Ignore the Django user model's is_active flag for login requests
MAGICLINK_IGNORE_IS_ACTIVE_FLAG = True
MAGICLINK_TOKEN_LENGTH = 100
MAGICLINK_VERIFY_INCLUDE_EMAIL = True
MAGICLINK_REQUIRE_SAME_BROWSER = False
MAGICLINK_REQUIRE_SAME_IP = False
MAGICLINK_ANONYMIZE_IP = True
MAGICLINK_TOKEN_USES = 1
MAGICLINK_LOGIN_REQUEST_TIME_LIMIT = 30  # In seconds
# Disable all other tokens for a user when a new token is requested
MAGICLINK_ONE_TOKEN_PER_USER = True
MAGICLINK_ANTISPAM_FORMS = False
MAGICLINK_ANTISPAM_FIELD_TIME = 1  # in seconds
MAGICLINK_LOGIN_VERIFY_URL = "magiclink:login_verify"
MAGICLINK_IGNORE_UNSUBSCRIBE_IF_USER = False

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "nifek", "static/")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

CRISPY_TEMPLATE_PACK = "bootstrap4"

AUTH_USER_MODEL = "accounts.User"
