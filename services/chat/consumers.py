from django.utils import timezone
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from chat.models.chat import Chat
from authn.rest.auth.serializers import UserSerializer

from .models import ChatMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return
        
        self.subid = self.scope["url_route"]["kwargs"]["subid"]
        self.room_group_name = f"chat_{self.subid}"
        
        # await self.mark_messages_as_read(self.scope["user"].id, self.subid)

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
        user = await self.get_user(sender_id)
        
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
        resp_save = await self.save_message(sender_id, self.subid, message)
        
        sender = UserSerializer(user).data

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": resp_save.message,
                "sender": sender,
                "created_at": resp_save.created_at.isoformat(),
                "sender_id": sender_id,  # ✅ include this
            }
        )

    # async def chat_message(self, event):
    #     await self.send(text_data=json.dumps(event))
    
    async def chat_message(self, event):
        is_mine = event["sender_id"] == self.scope["user"].id
        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "message": event["message"],
            "sender": event["sender"],
            "created_at": event["created_at"],
            "is_mine": is_mine,
        }))
        
    # async def typing_indicator(self, event):
    #     await self.send(text_data=json.dumps({
    #         "type": "typing",
    #         "sender_id": event["sender_id"],
    #         "is_typing": event["is_typing"]
    #     }))


    @database_sync_to_async
    def save_message(self, sender_id, subid, message):
        chat = Chat.objects.get(subid=subid)
        return ChatMessage.objects.create(
            sender_id=sender_id,
            chat=chat,
            message=message
        )
        
    # @database_sync_to_async
    # def mark_messages_as_read(self, user_id, subid):
    #     ChatMessage.objects.filter(
    #         subid=subid, is_read=False
    #     ).exclude(sender_id=user_id).update(is_read=True)

    @database_sync_to_async
    def get_user(self, sender_id):
        return User.objects.filter(id=sender_id).first()