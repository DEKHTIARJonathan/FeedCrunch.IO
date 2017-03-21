from django.core.management.base import BaseCommand
from django.utils.six import PY2

import cryptography.fernet


class Command(BaseCommand):
    help = 'Generates a new Fernet encryption key'

    def handle(self, *args, **options):
        key = cryptography.fernet.Fernet.generate_key()
        if PY2:
            self.stdout.write(key)
        else:
            self.stdout.write(key, ending=b'\n')
