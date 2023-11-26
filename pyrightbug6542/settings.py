import sys
from os import environ as env
from pathlib import Path

from django.db.models import CharField, ForeignKey
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet


def make_generic(cls):
    try:
        cls.__class_getitem__  # noqa
    except AttributeError:
        cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)


for cls in [QuerySet, BaseManager, ForeignKey, CharField]:
    make_generic(cls)

del make_generic

HOST_URL = env.get("HOST_URL", "http://localhost:8000")
CSRF_TRUSTED_ORIGINS = [HOST_URL]

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
SECRET_KEY = env.get("SECRET_KEY", "tqeTeQB3u-MqvQ9ONUrLdANGcpSsV,MA")


def parse_bool(key: str, default: bool) -> bool:
    value = env.get(key)
    if value is None:
        return default
    else:
        return str(value).lower().strip() in ("true", "yes", "on")


FORCE_TESTING = parse_bool("FORCE_TESTING", False)
TESTING = FORCE_TESTING or "py.test" in " ".join(sys.argv)
COLLECT_STATIC = "collectstatic" in " ".join(sys.argv)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = parse_bool("DEBUG", not TESTING)
IN_PRODUCTION = not DEBUG and not TESTING and not COLLECT_STATIC

ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS = ["demo"]

# Middleware
MIDDLEWARE = []
ROOT_URLCONF = "pyrightbug6542.urls"

WSGI_APPLICATION = "pyrightbug6542.wsgi.application"
ASGI_APPLICATION = "pyrightbug6542.asgi.application"

# For the internal dashboard big numbers.
USE_THOUSAND_SEPARATOR = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.get("DB_HOST", "127.0.0.1"),
        "PORT": env.get("DB_PORT", "5432"),
        "USER": env.get("DB_USER", env.get("POSTGRES_USER", "postgres")),
        "PASSWORD": env.get("DB_PASSWORD", env.get("POSTGRES_PASSWORD")),
        "NAME": env.get("DB_NAME", "pyrightbug6542"),
    }
}

# Django 3.2+ backwards compatible setting for models without a primary_key:
# https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys  # noqa
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
