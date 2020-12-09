#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    local_file = Path("sample_api/settings/local.py")
    if local_file.is_file():
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "sample_api.settings.local")
    else:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "sample_api.settings.production")
    try:
        from django.core.management import execute_from_command_line  # noqa
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    try:
        execute_from_command_line(sys.argv)
    except ImportError as e:
        print(e)


if __name__ == '__main__':
    main()
