from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.random_quote, name='random_quote'),
    path('add/', views.add_quote, name='add_quote'),
    path('popular/', views.popular_quotes, name='popular_quotes'),
]