from django.contrib import admin

from authn.models.user import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('subid', 'email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser',)
    list_filter = ('is_active', 'is_staff', 'is_superuser',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def save_model(self, request, obj, form, change):
        # If the password was changed in the admin, hash it
        password = form.cleaned_data.get('password')
        if password and (not obj.pk or 'password' in form.changed_data):
            obj.set_password(password)
        super().save_model(request, obj, form, change)