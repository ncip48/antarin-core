# -*- coding: utf-8 -*-
"""
Django Channels WebSocket consumer for real-time chat functionality.

This module handles WebSocket connections for chat rooms, allowing users to send
and receive messages in real-time. It manages user authentication, message
broadcasting, and database interactions asynchronously.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone

from chat.models.chat import Chat
from authn.rest.auth.serializers import UserSerializer
from .models import ChatMessage

# Get the custom User model
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """
    A WebSocket consumer that handles real-time chat communication.

    This consumer manages the lifecycle of a WebSocket connection for a specific
    chat room. It handles user authentication, joining/leaving chat rooms,
    receiving and broadcasting messages, and typing indicators.

    Attributes:
        subid (str): A unique identifier for the chat room.
        room_group_name (str): The name of the channel layer group for the chat room.
    """

    async def connect(self):
        """
        Handles a new WebSocket connection.

        This method is called when a client attempts to establish a WebSocket
        connection. It authenticates the user, extracts the chat room subid from
        the URL, and adds the connection to a channel layer group. If the user

        is not authenticated, the connection is rejected.
        """
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close()
            return

        self.subid = self.scope["url_route"]["kwargs"]["subid"]
        self.room_group_name = f"chat_{self.subid}"

        # Add the channel to the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Mark existing messages as read for the current user
        await self.mark_messages_as_read(user.id, self.subid)

    async def disconnect(self, close_code):
        """
        Handles a WebSocket disconnection.

        This method is called when a WebSocket connection is closed. It removes the
        channel from the channel layer group to stop broadcasting messages to it.
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Receives a message from the WebSocket.

        This method processes incoming data from the client. It can handle
        different event types, such as new chat messages or typing indicators,
        based on the 'type' key in the received JSON data.
        """
        try:
            data = json.loads(text_data)
            message_type = data.get("type", "chat_message")

            if message_type == "typing":
                await self.handle_typing_indicator(data)
            elif message_type == "chat_message":
                await self.handle_chat_message(data)

        except json.JSONDecodeError:
            # Handle malformed JSON
            pass
        except Exception as e:
            # Log other potential errors
            print(f"Error receiving websocket message: {e}")


    async def handle_chat_message(self, data):
        """
        Handles incoming chat messages.

        It saves the message to the database and then broadcasts it to the
        entire group.
        """
        message = data.get("message", "").strip()
        if not message:
            return  # Ignore empty or whitespace-only messages

        sender_id = self.scope["user"].id
        user = await self.get_user(sender_id)
        if not user:
            return # User not found, should not happen if authenticated

        # Save the new message to the database
        saved_message = await self.save_message(sender_id, self.subid, message)

        # Serialize the sender's data
        sender_data = UserSerializer(user).data

        # Broadcast the message to the channel layer group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_message",
                "message": saved_message.message,
                "sender": sender_data,
                "created_at": saved_message.created_at.isoformat(),
                "sender_id": sender_id,
            },
        )

    async def handle_typing_indicator(self, data):
        """
        Handles typing indicator events from the client.

        Broadcasts the typing status of a user to the other members of the
        chat room.
        """
        sender_id = self.scope["user"].id
        is_typing = data.get("is_typing", False)
        
        user = await self.get_user(sender_id)
        if not user:
            return # User not found, should not happen if authenticated
        
        sender_data = UserSerializer(user).data

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "typing_event",
                "sender": sender_data,
                "sender_id": sender_id,
                "is_typing": is_typing,
            },
        )

    async def broadcast_message(self, event):
        """
        Sends a broadcasted chat message to the client.

        This method is called by the channel layer for each consumer in the
        group. It determines if the message was sent by the current user
        ('is_mine') and sends the formatted message down to the client.
        """
        is_mine = event["sender_id"] == self.scope["user"].id
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_message",
                    "message": event["message"],
                    "sender": event["sender"],
                    "created_at": event["created_at"],
                    "is_mine": is_mine,
                }
            )
        )

    async def typing_event(self, event):
        """
        Sends a typing indicator event to the client.

        This method forwards the typing status to the client, excluding the
        originating sender to prevent them from seeing their own typing status.
        """
        if event["sender_id"] != self.scope["user"].id:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "typing",
                        "sender": event["sender"],
                        "is_typing": event["is_typing"],
                    }
                )
            )

    # -------------------------------------------------------------------------
    # Database Operations
    # -------------------------------------------------------------------------

    @database_sync_to_async
    def save_message(self, sender_id, subid, message):
        """
        Saves a new chat message to the database.

        Args:
            sender_id (int): The ID of the user sending the message.
            subid (str): The unique identifier for the chat.
            message (str): The content of the message.

        Returns:
            ChatMessage: The newly created ChatMessage instance.
        """
        chat = Chat.objects.get(subid=subid)
        return ChatMessage.objects.create(
            sender_id=sender_id, chat=chat, message=message
        )

    @database_sync_to_async
    def mark_messages_as_read(self, user_id, subid):
        """
        Marks all unread messages in a chat as read for a given user.

        This excludes messages sent by the user themselves.

        Args:
            user_id (int): The ID of the user for whom to mark messages.
            subid (str): The unique identifier of the chat.
        """
        chat = Chat.objects.get(subid=subid)
        ChatMessage.objects.filter(
            chat=chat, is_read=False
        ).exclude(sender_id=user_id).update(is_read=True)

    @database_sync_to_async
    def get_user(self, user_id):
        """
        Retrieves a user instance from the database by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The User instance, or None if not found.
        """
        return User.objects.filter(id=user_id).first()
