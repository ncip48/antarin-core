import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return
        
        self.booking_id = self.scope["url_route"]["kwargs"]["booking_id"]
        self.room_group_name = f"chat_{self.booking_id}"
        
        await self.mark_messages_as_read(self.scope["user"].id, self.booking_id)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender_id = self.scope["user"].id
        
        # Handle typing indicator
        # if data.get("type") == "typing":
        #     await self.channel_layer.group_send(
        #         self.room_group_name,
        #         {
        #             "type": "typing_indicator",
        #             "sender_id": sender_id,
        #             "is_typing": data.get("is_typing", False),
        #         }
        #     )
        #     return

        # Handle actual chat message
        message = data.get("message", "").strip()
        if not message:
            return  # Ignore empty messages

        # Save message
        await self.save_message(sender_id, self.booking_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": sender_id,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
        
    # async def typing_indicator(self, event):
    #     await self.send(text_data=json.dumps({
    #         "type": "typing",
    #         "sender_id": event["sender_id"],
    #         "is_typing": event["is_typing"]
    #     }))


    @database_sync_to_async
    def save_message(self, sender_id, booking_id, message):
        return ChatMessage.objects.create(
            sender_id=sender_id,
            trip_id=booking_id,
            message=message
        )
        
    @database_sync_to_async
    def mark_messages_as_read(self, user_id, booking_id):
        ChatMessage.objects.filter(
            trip_id=booking_id, is_read=False
        ).exclude(sender_id=user_id).update(is_read=True)
