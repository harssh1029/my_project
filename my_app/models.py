from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=10, unique=True)
    user_type = models.CharField(max_length=20, default='individual')
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=50)
    broker = models.CharField(max_length=50, default='ZERODHA')
    password = models.CharField(max_length=128)
    mobile = models.CharField(max_length=15, blank=True, null=True)  # Mobile number field
    date_of_birth = models.DateField(blank=True, null=True)

class HistoricalData(models.Model):
    date = models.DateTimeField()
    price = models.FloatField()
    symbol = models.CharField(max_length=50)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='user_id')  # Use 'user_id' for reference
    tradingsymbol = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default='Placed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user_name} - {self.tradingsymbol} - {self.status}"

