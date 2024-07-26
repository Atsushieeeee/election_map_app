from django.shortcuts import render
from django.http import JsonResponse
from .models import City, Vote
from datetime import datetime

def city_data(request):
    cities = City.objects.all()
    data = [{
        'name': city.name,
        'polygon': city.polygon,
    } for city in cities]
    return JsonResponse(data, safe=False)

def get_votes_by_city(request):
    city = request.GET.get('city')
    election_date = request.GET.get('election_date', '2024-07-07')
    region = request.GET.get('region', '東京')  # デフォルトの地域を東京に設定

    if city and election_date:
        votes = Vote.objects.filter(city=city, election_date=election_date, region=region)
        votes_data = [
            {
                'candidate_name': vote.candidate_name,
                'party_name': vote.party_name,
                'city': vote.city,
                'votes': vote.votes,
                'election_date': vote.election_date,
                'region': vote.region
            }
            for vote in votes
        ]
        return JsonResponse(votes_data, safe=False)
    return JsonResponse({'error': 'City and election_date parameters are required'}, status=400)