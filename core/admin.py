from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'username')
    readonly_fields = ('date_joined', 'last_login', 'password')
    fieldsets = (
        ('Authorization', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',  'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
admin.site.register(User, UserAdmin)