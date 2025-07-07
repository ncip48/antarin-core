from django.contrib import admin

from chat.models.chat_message import ChatMessage

# Register your models here.
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ChatMessage._meta.fields]
    search_fields = ['id', 'name']
    list_filter = ['created_at']
    ordering = ['-created_at']

