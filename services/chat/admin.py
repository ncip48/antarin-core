from django.contrib import admin

from chat.models import ChatMessage, Chat, ChatParticipant

# Register your models here.
@admin.register(Chat)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Chat._meta.fields]
    search_fields = ['id', 'name']
    list_filter = ['created_at']
    ordering = ['-created_at']
    
@admin.register(ChatParticipant)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ChatParticipant._meta.fields]
    search_fields = ['id', 'user.first_name', 'user.last_name', 'user.email']
    list_filter = ['joined_at']
    ordering = ['-joined_at']
    
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ChatMessage._meta.fields]
    search_fields = ['id', 'name']
    list_filter = ['created_at']
    ordering = ['-created_at']

