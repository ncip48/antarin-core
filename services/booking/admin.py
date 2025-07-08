from django.contrib import admin

# Register your models here.
from .models.trip import Trip

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "pickup_point", "driver", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer__username", "driver__user__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

