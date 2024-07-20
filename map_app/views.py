from django.shortcuts import render
from django.http import JsonResponse
from .models import City

def city_data(request):
    cities = City.objects.all()
    data = [{
        'name': city.name,
        'polygon': city.polygon,
    } for city in cities]
    return JsonResponse(data, safe=False)