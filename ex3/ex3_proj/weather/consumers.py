import time
import json

from django.forms.models import model_to_dict
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Weather

class WeatherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "weather"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from room group
    async def weather_message(self, event):
        timestamp = time.time()
        message = event.get("message")
        if message == "update":
            weathers = await database_sync_to_async(lambda: Weather.objects.all())()
            weathers = [
                model_to_dict(weather, fields=["location", "data"])
                for weather in weathers
            ]
        else:
            weathers = []

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"timestamp": timestamp, "message": message, "weathers": weathers}
            )
        )
