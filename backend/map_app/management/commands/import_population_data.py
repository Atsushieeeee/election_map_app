from django.core.management.base import BaseCommand, CommandError
import os
import csv
from map_app.models import PopulationDistribution

def parse_int(value):
    try:
        return int(value)
    except ValueError:
        return 0

class Command(BaseCommand):
    help = 'Import population distribution data from a CSV file'

    def handle(self, *args, **kwargs):
        file_path = 'data/population.csv'  # 固定のファイルパス

        if not os.path.isfile(file_path):
            raise CommandError(f"File {file_path} does not exist")

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                PopulationDistribution.objects.create(
                    region_code=row['地域コード'],
                    region=row['地域'],
                    age_group=row['年齢'],
                    total_population=parse_int(row['総数／計(人)']),
                    total_men=parse_int(row['総数／男(人)']),
                    total_women=parse_int(row['総数／女(人)']),
                    japanese_total=parse_int(row['日本人／計(人)']),
                    japanese_men=parse_int(row['日本人／男(人)']),
                    japanese_women=parse_int(row['日本人／女(人)']),
                    foreign_total=parse_int(row['外国人／計(人)']),
                    foreign_men=parse_int(row['外国人／男(人)']),
                    foreign_women=parse_int(row['外国人／女(人)']),
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV'))