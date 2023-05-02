from django.contrib import admin
from .models import GoalCategory, Goal, GoalComment

class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'user', 'is_deleted')
    list_display_links = ('title', )
    search_fields = ('title', )
    list_filter = ('is_deleted', )
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(GoalCategory, GoalCategoryAdmin) 
admin.site.register(Goal)
admin.site.register(GoalComment)