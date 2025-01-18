from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('load-historical-data/', views.load_historical_data, name='load_historical_data'),
    path('api/historical-data/', views.get_historical_data, name='get_historical_data'),
]
