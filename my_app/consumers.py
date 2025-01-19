# consumers.py
import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class StockPriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "stocks"
        self.room_group_name = "stocks_group"

        # Get the channel layer (this ensures it's correctly set up in settings)
        self.channel_layer = self.channel_layer

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

        # Initial dummy stock prices
        self.stock_prices = {
            'AAPL': 150.0,
            'GOOGL': 2750.0,
            'AMZN': 3500.0,
            'TSLA': 1000.0,
            'MSFT': 300.0
        }

        # Send periodic updates
        await self.send_stock_price_periodically()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def send_stock_price_periodically(self):
        while True:
            # Simulate stock price update (increasing by 1%)
            updated_prices = {symbol: price + (price * 0.01) for symbol, price in self.stock_prices.items()}
            self.stock_prices = updated_prices

            # Send updated stock prices to WebSocket clients
            await self.send(text_data=json.dumps({
                'stocks': [{'symbol': symbol, 'price': round(price, 2)} for symbol, price in self.stock_prices.items()]
            }))

            await asyncio.sleep(5)
