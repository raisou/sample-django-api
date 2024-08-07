from argparse import ArgumentParser
from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "[DANGER] Reset database and load demo data into database"

    FIXTURES = ("users",)

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            dest="force",
            default=False,
            help="Used to deploy recette or dev. Don't use it in production!",
        )

    def handle(self, *_args: Any, **options: Any) -> None:
        force = options.get("force", False)

        if not force:
            confirm = input(
                """
    [DANGER] You have requested to reload data.
    [DANGER] This will IRREVERSIBLY DESTROY all data currently in the database.
    [DANGER] Are you sure you want to do this?
    [DANGER]
    [DANGER] Type 'yes' to continue, or 'no' to cancel: """
            )

            if confirm != "yes":
                return

        self.log("--- Emptying database ------------------")
        self.drop_tables()
        self.log("--- Creating database structure --------")
        call_command("migrate", interactive=False)

        self.log("--- Loading base data ------------------")
        self.loaddata(*self.FIXTURES)

    def log(self, message: str) -> None:
        """Displays a message via stdout."""
        self.stdout.write(message)

    def drop_tables(self) -> None:
        """Drop all database tables"""
        tables = connection.introspection.table_names()
        cursor = connection.cursor()
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")

    def loaddata(self, *args: Any) -> None:
        call_command("loaddata", *args)
