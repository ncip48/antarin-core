from django.contrib import admin
from driver.models.driver import Driver

# Register your models here.
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_available", "location", "last_active")
    list_filter = ("is_available",)
    search_fields = ("user__username", "user__email")
    readonly_fields = ("last_active",)
    ordering = ("-last_active",)