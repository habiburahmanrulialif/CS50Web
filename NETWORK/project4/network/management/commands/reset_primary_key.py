from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Reset primary key sequence to a specific value'

    def handle(self, *args, **options):
        table_name = 'network_Post'  # Replace with your actual app and model name
        sequence_name = f"{table_name}_id_seq"
        reset_value = 1  # Replace with the desired starting value

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT setval('{sequence_name}', {reset_value}, false)")

        self.stdout.write(self.style.SUCCESS(f"Primary key sequence for {table_name} reset to {reset_value}"))