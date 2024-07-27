from django.urls import path
from .views import get_votes_by_city, get_population_distribution, population_gender_distribution, fertility_rate_by_region

urlpatterns = [
    path('votes/', get_votes_by_city, name='get_votes_by_city'),
    path('population_distribution/', get_population_distribution, name='get_population_distribution'),
    path('population_gender_distribution/', population_gender_distribution, name='population_gender_distribution'),
    path('fertility_rate/', fertility_rate_by_region, name='fertility_rate_by_region'),
]
