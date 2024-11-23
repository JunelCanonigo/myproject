from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Drivers, CustomUser

# Customize the CustomUser admin to include the 'role' field
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'email', 'role']  # Include the role in the list display
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Add the role field in the user edit form
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),  # Add the role field in the user creation form
    )

# Register the CustomUser with the customized UserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

# Customize the Drivers admin
class DriversAdmin(admin.ModelAdmin):
    list_display = ['plate_number', 'first_name', 'last_name', 'user']  # Display relevant fields
    search_fields = ['plate_number', 'first_name', 'last_name']  # Add search functionality
    list_filter = ['user__role']  # Filter by the role of the associated user

# Register the Drivers model with the custom admin configuration
admin.site.register(Drivers, DriversAdmin)
