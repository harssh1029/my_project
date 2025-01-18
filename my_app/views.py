from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Max
from .models import User, HistoricalData
import csv
import os

# Function to load data from the uploaded historical file
def load_historical_data(request):
    try:
        file_path = "my_app/historical_prices.csv"  # Replace with actual file path
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    HistoricalData.objects.create(
                        date=row['date'],
                        price=row['price'],
                        symbol=row['instrument_name']
                    )
        return JsonResponse({"status": "success", "message": "Historical data loaded."})
    except Exception as e:
        s = str(e)

# Registration View
def register(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Generate unique user_id
        last_user = User.objects.aggregate(Max('id'))['id__max']
        user_id = f"a{(last_user or 0) + 1}"

        User.objects.create(
            user_id=user_id,
            user_name=user_name,
            email=email,
            password=password
        )
        return redirect('login')

    return render(request, 'register.html')

# Login View
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_id'] = user.user_id
            return redirect('dashboard')
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

# Dashboard View
def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(user_id=user_id)
    holding_data = [
        {
            "tradingsymbol": "GOLDBEES",
            "exchange": "BSE",
            "isin": "INF204KB17I5",
            "quantity": "2",
            "authorised_date": "2021-06-08 00:00:00",
            "average_price": "40.67",
            "last_price": "42.47",
            "close_price": "42.28",
            "pnl": "3.5999999999999943",
            "day_change": "0.18999999999999773",
            "day_change_percentage": "0.44938505203405327"
        },
        {
            "tradingsymbol": "IDEA",
            "exchange": "NSE",
            "isin": "INE669E01016",
            "quantity": 5,
            "authorised_date": "2021-06-08 00:00:00",
            "average_price": 8.466,
            "last_price": 10,
            "close_price": 10.1,
            "pnl": 7.6700000000000035,
            "day_change": -0.09999999999999964,
            "day_change_percentage": -0.9900990099009866
        }
    ]
    return render(request, 'dashboard.html', {'profile': user, 'holding_data': holding_data})

def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(user_id=user_id)
    return render(request, 'profile.html', {'profile': user})

# API to fetch historical data
def get_historical_data(request):
    symbol = request.GET.get('symbol')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    data = HistoricalData.objects.filter(
        symbol=symbol,
        date__range=[from_date, to_date]
    ).values('date', 'price')

    return JsonResponse(list(data), safe=False)
