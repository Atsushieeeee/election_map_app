from django.urls import path
from .views import get_votes_by_city, get_population_distribution

urlpatterns = [
    path('votes/', get_votes_by_city, name='get_votes_by_city'),
    path('population_distribution/', get_population_distribution, name='get_population_distribution'),
]
