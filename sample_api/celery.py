import os
from pathlib import Path

from celery import Celery


# set the default Django settings module for the 'celery' program.
local_file = Path("sample_api/settings/local.py")
if local_file.is_file():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sample_api.settings.local")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sample_api.settings.production")

app = Celery("sample_api")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
