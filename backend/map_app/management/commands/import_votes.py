import csv
from django.core.management.base import BaseCommand
from map_app.models import Vote

class Command(BaseCommand):
    help = 'Import votes data from CSV file'

    def handle(self, *args, **kwargs):
        # 指定されたファイルパスを使用
        file_path = 'data/r6_tochiji_kaihyo_kouhoshatokuhyo.csv'
        election_date = '2024-07-07'  # 固定値として設定
        region = '東京都'  # 固定値として設定

        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)  # ヘッダー行をスキップ
            # 1行目と2行目を組み合わせて姓名を作成
            last_names = next(reader)[2:]  # 1行目（苗字）のデータ
            first_names = next(reader)[2:]   # 2行目（名前）のデータ

            # 政党名
            parties = next(reader)[2:]
            # データ行
            for row in reader:
                city = row[0]
                votes = row[2:]

                for i, vote_count in enumerate(votes):
                    try:
                        vote_count_float = float(vote_count)
                        Vote.objects.create(
                            candidate_name=f"{last_names[i]} {first_names[i]}",
                            party_name=parties[i],
                            city=city,
                            votes=vote_count_float,
                            election_date=election_date,
                            region=region
                        )
                    except ValueError:
                        # Skip non-numeric vote counts
                        continue
        self.stdout.write(self.style.SUCCESS('Successfully imported votes data'))