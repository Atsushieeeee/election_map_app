import json
from django.core.management.base import BaseCommand
from map_app.models import City

class Command(BaseCommand):
    help = 'Import City data from GeoJSON'

    def handle(self, *args, **kwargs):
        with open('path_to_your_geojson_file.json') as f:
            data = json.load(f)
            for feature in data['features']:
                name = feature['properties']['name']
                polygon = feature['geometry']
                City.objects.create(name=name, polygon=polygon)