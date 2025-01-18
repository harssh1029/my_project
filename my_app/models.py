from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=10, unique=True)
    user_type = models.CharField(max_length=20, default='individual')
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=50)
    broker = models.CharField(max_length=50, default='ZERODHA')
    password = models.CharField(max_length=128)

class HistoricalData(models.Model):
    date = models.DateTimeField()
    price = models.FloatField()
    symbol = models.CharField(max_length=50)
