# management/commands/import_income_distribution.py
import csv
import os
from django.core.management.base import BaseCommand, CommandError
from map_app.models import IncomeDistribution

class Command(BaseCommand):
    help = 'Import income distribution data from a CSV file'

    def handle(self, *args, **kwargs):
        file_path = 'data/income_distribution.csv'

        if not os.path.isfile(file_path):
            raise CommandError(f"File {file_path} does not exist")

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                IncomeDistribution.objects.create(
                    region_code=row['地域 コード'],
                    region=row['地域'],
                    year = int(row['時間軸(年次)'].replace('年', '')),
                    income_class=row['世帯の年間収入階級'],
                    household_count=int(row['普通世帯数【世帯】'].replace(',', ''))
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV'))