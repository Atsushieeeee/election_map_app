from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from .models import City, Vote, PopulationDistribution, FertilityRate, IncomeDistribution


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
        total_votes = sum(vote.votes for vote in votes)
        votes_data = [
            {
                'candidate_name': vote.candidate_name,
                'party_name': vote.party_name,
                'city': vote.city,
                'votes': vote.votes,
                'election_date': vote.election_date,
                'region': vote.region,
                'total_votes': total_votes
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

        # '総数' のデータを取得
        total_data = data.filter(age_group='総数').first()
        if total_data:
            total_population = total_data.total_population
            total_men = total_data.total_men
            total_women = total_data.total_women
        else:
            total_population = total_men = total_women = None

        # '総数' を除いたデータを取得
        age_groups = data.exclude(age_group='総数').values('age_group', 'total_population', 'total_men', 'total_women')

        response_data = {
            'age_groups': list(age_groups),
            'total_population': total_population,
            'total_men': total_men,
            'total_women': total_women,
        }
        return JsonResponse(response_data, safe=False)
    except PopulationDistribution.DoesNotExist:
        return JsonResponse({'error': 'データが見つかりません。'}, status=404)


def fertility_rate_by_region(request):
    region = request.GET.get('region')
    if not region:
        return JsonResponse({'error': '地域が指定されていません。'}, status=400)

    try:
        data = FertilityRate.objects.filter(region=region).values('year', 'rate')
        response_data = [{'year': item['year'], 'rate': item['rate']} for item in data]
        return JsonResponse(response_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def income_distribution(request):
    region = request.GET.get('region')
    
    income_data = IncomeDistribution.objects.filter(region=region).exclude(income_class='総数')
    income_distribution_data = [
        {'income_class': data.income_class, 'household_count': data.household_count}
        for data in income_data
    ]

    return JsonResponse(income_distribution_data, safe=False)