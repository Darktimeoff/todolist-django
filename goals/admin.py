from django.contrib import admin
from .models import GoalCategory, Goal, GoalComment, Board, BoardParticipant

class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'user', 'is_deleted')
    list_display_links = ('title', )
    search_fields = ('title', )
    list_filter = ('is_deleted', )
    readonly_fields = ('created', 'updated')

admin.site.register(GoalCategory, GoalCategoryAdmin) 
admin.site.register(Goal)
admin.site.register(GoalComment)
admin.site.register(Board)
admin.site.register(BoardParticipant)