from django.contrib import admin
from notification.models import Notification, NotificationRecipient

# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Notification._meta.fields]
    search_fields = ['subid', 'title', 'body']
    list_filter = ['created_at']
    ordering = ['-created_at']
    
@admin.register(NotificationRecipient)
class NotificationRecipientAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NotificationRecipient._meta.fields]
    search_fields = ['subid', 'user.first_name', 'user.last_name', 'user.email']