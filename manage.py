#!/usr/bin/env python
import logging
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sample_api.settings.local")

    from django.core.management import execute_from_command_line

    try:
        execute_from_command_line(sys.argv)
    except ImportError:
        logging.exception("Error found")


if __name__ == "__main__":
    main()
