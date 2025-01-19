from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from .models import User, HistoricalData
import csv
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Order
import json


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


def register(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        mobile = request.POST['mobile']
        date_of_birth = request.POST['date_of_birth']


        # Generate unique user_id
        last_user = User.objects.aggregate(Max('id'))['id__max']
        user_id = f"a{(last_user or 0) + 1}"

        User.objects.create(
            user_id=user_id,
            user_name=user_name,
            email=email,
            password=password,
            mobile=mobile,
            date_of_birth=date_of_birth
        )
        return redirect('login')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_id'] = user.user_id
            request.session['user'] = user.user_name
            return redirect('dashboard')
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


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


def get_historical_data(request):
    symbol = request.GET.get('symbol')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    data = HistoricalData.objects.filter(
        symbol=symbol,
        date__range=[from_date, to_date]
    ).values('date', 'price')

    return JsonResponse(list(data), safe=False)


@csrf_exempt
def place_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tradingsymbol = data.get("tradingsymbol")
        price = data.get("price")
        quantity = data.get("quantity")
        user_id = request.session.get('user_id')

        # Fetch the User object based on user_id
        user = get_object_or_404(User, user_id=user_id)
        if not tradingsymbol or not price or not quantity:
            return JsonResponse({"success": False, "error": "Missing required fields"}, status=400)

        # Create the order and associate it with the user
        order = Order.objects.create(
            user=user,
            tradingsymbol=tradingsymbol,
            price=price,
            quantity=quantity,
            status="Placed",
        )

        return JsonResponse({
            "success": True,
            "order": {
                "tradingsymbol": order.tradingsymbol,
                "price": order.price,
                "quantity": order.quantity,
                "status": order.status,
            },
        })

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def get_user_orders(request):
    user_id = request.session['user_id']
    orders = Order.objects.filter(user__user_id=user_id)

    # Format order data
    order_data = [
        {
            'tradingsymbol': order.tradingsymbol,
            'price': order.price,
            'quantity': order.quantity,
            'status': order.status,
        }
        for order in orders
    ]
    return JsonResponse({"success": True, "orders": order_data})
