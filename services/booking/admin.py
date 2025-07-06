from django.contrib import admin

# Register your models here.
from .models.driver import Driver
from .models.booking_request import BookingRequest

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_available", "location", "last_active")
    list_filter = ("is_available",)
    search_fields = ("user__username", "user__email")
    readonly_fields = ("last_active",)
    ordering = ("-last_active",)

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "pickup_point", "driver", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer__username", "driver__user__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

