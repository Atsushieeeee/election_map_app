from django.core.management.base import BaseCommand, CommandError
import os
import csv
from map_app.models import FertilityRate

class Command(BaseCommand):
    help = 'Import fertility rate data from a CSV file'

    def handle(self, *args, **kwargs):
        file_path = 'data/04goukei.csv'  # 固定のファイルパス

        if not os.path.isfile(file_path):
            raise CommandError(f"File {file_path} does not exist")

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            years = reader.fieldnames[1:]  # 年の列名を取得
            for row in reader:
                region = row['']
                for year in years:
                    rate = row[year].strip()  # 前後の空白を除去
                    # データが '-' または空文字なら None にする
                    if rate in ['-', '']:
                        rate = None
                    else:
                        try:
                            rate = float(rate)
                        except ValueError:
                            rate = None  # 万が一、他の不正な値があった場合にも対応
                    FertilityRate.objects.create(
                        year=year,
                        region=region,
                        rate=rate
                    )

        self.stdout.write(self.style.SUCCESS('Successfully imported fertility rate data from CSV'))
