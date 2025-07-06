import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DriverConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.driver_id = self.scope['user'].id
        self.group_name = f"driver_{self.driver_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        from booking.tasks import accept_booking_task, update_booking_status_task
        data = json.loads(text_data)
        action = data.get("action")

        if action == "accept_booking":
            booking_id = data.get("booking_id")
            driver_id = self.driver_id
            accept_booking_task.delay(booking_id, driver_id)

            await self.send(text_data=json.dumps({
                "message": "Permintaan diterima, menunggu konfirmasi sistem..."
            }))

        elif action == "start_trip":
            booking_id = data.get("booking_id")
            update_booking_status_task.delay(booking_id, "on_trip", self.driver_id)

        elif action == "complete_trip":
            booking_id = data.get("booking_id")
            update_booking_status_task.delay(booking_id, "completed", self.driver_id)

    async def driver_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))


class CustomerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["user"].id
        self.group_name = f"user_{self.user_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "ping":
            await self.send(text_data=json.dumps({"message": "pong pong pong"}))

    async def user_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))