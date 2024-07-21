"""
Custom Django Command for starting up server. 
The Postgres Database needs to be spun up first before the server, or
else the server will fail to connect and start up.
"""
from psycopg import OperationalError as PsycopgOpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

import time


class Command(BaseCommand):
    """
    Command to check if the server can setup a connection.
    The server will sleep for one second if it fails to connect.
    Loops until it succeeds. 
    """
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycopgOpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
        