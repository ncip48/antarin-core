from django.contrib import admin
from driver.models.driver import Driver

# Register your models here.
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        "subid",
        "user",
        "nik",
        "is_available",
        "is_verified",
        "location",
        "last_active",
        "registered_at",
    )
    list_filter = ("is_available", "is_verified")
    search_fields = ("user__username", "user__email", "nik")
    readonly_fields = ("last_active", "registered_at")
    ordering = ("-last_active",)