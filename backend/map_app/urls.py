from django.urls import path
from .views import get_votes_by_city

urlpatterns = [
    path('votes/', get_votes_by_city, name='get_votes_by_city'),
]
