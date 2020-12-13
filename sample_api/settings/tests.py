import os
from pathlib import Path

from .defaults import *  # noqa


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "travis_ci",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

SECRET_KEY = "zj6ay3l7s^ga3!*!zi(s81+jj01eblt=wxzzd3=__n0wh0a5uw"

LANGUAGE_CODE = "fr-FR"

TIME_ZONE = "Europe/Paris"

STATIC_ROOT = os.path.join(BASE_DIR, "static/static/")

MEDIA_ROOT = os.path.join(BASE_DIR, "static/media/")

MEDIA_URL = "/media/"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Task are always run in sync mode for testing purposes
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
