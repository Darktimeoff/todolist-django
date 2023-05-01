from django.contrib import admin
from .models import GoalCategory

class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'user')

admin.site.register(GoalCategory, GoalCategoryAdmin)