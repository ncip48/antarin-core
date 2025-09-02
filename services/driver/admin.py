from django.contrib import admin
from driver.models.driver import Driver

# Register your models here.
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        "subid",
        "user",
        "phone_number",
        "address",
        "is_verified",
        "location",
        "last_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_verified",)
    search_fields = ("user__username", "user__email", "phone_number")
    readonly_fields = ("last_active", "created_at", "updated_at")
    ordering = ("-last_active",)