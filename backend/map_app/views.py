from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from .models import City, Vote, PopulationDistribution


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


def get_population_distribution(request):
    region = request.GET.get('region')
    
    if region:
        data = PopulationDistribution.objects.filter(region=region).order_by('age_group')
        age_groups = []
        total_population = None

        for item in data:
            if item.age_group == '総数':
                total_population = item.total_population
            else:
                age_groups.append({
                    'age_group': item.age_group,
                    'total_population': item.total_population,
                })

        return JsonResponse({
            'age_groups': age_groups,
            'total_population': total_population,
        })
    return JsonResponse({'error': 'Region parameter is required'}, status=400)


def population_gender_distribution(request):
    region = request.GET.get('region')
    if not region:
        return JsonResponse({'error': '地域が指定されていません。'}, status=400)

    try:
        data = PopulationDistribution.objects.filter(region=region)
        age_groups = data.values('age_group', 'total_population', 'total_men', 'total_women')
        total_population = data.aggregate(total_population=Sum('total_population'))['total_population']
        total_men = data.aggregate(total_men=Sum('total_men'))['total_men']
        total_women = data.aggregate(total_women=Sum('total_women'))['total_women']

        response_data = {
            'age_groups': list(age_groups),
            'total_population': total_population,
            'total_men': total_men,
            'total_women': total_women,
        }
        return JsonResponse(response_data, safe=False)
    except PopulationDistribution.DoesNotExist:
        return JsonResponse({'error': 'データが見つかりません。'}, status=404)