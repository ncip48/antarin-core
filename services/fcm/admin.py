from django.contrib import admin

from fcm.models.fcm_device import FCMDevice

# Register your models here.
@admin.register(FCMDevice)
class FCMDeviceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FCMDevice._meta.fields]
    search_fields = ['id', 'name']
    list_filter = ['created_at']
    ordering = ['-created_at']