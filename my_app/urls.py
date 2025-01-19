from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('load-historical-data/', views.load_historical_data, name='load_historical_data'),
    path('api/historical-data/', views.get_historical_data, name='get_historical_data'),
    path('place-order/', views.place_order, name='place_order'),
    path('get-user-orders/', views.get_user_orders, name='get_user_orders'),
]
