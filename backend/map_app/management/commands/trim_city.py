from django.core.management.base import BaseCommand
from map_app.models import Vote

class Command(BaseCommand):
    help = 'Trim whitespace from city names in Vote model'

    def handle(self, *args, **kwargs):
        votes = Vote.objects.all()
        for vote in votes:
            vote.city = vote.city.strip()
            vote.save()
        self.stdout.write(self.style.SUCCESS('Successfully trimmed city names'))
