from django.contrib import admin
from .models import GoalCategory, Goal, GoalComment

class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'user')

admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal)
admin.site.register(GoalComment)