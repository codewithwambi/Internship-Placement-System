from django.contrib import admin
from .models import LogbookEntry, SupervisionComment

@admin.register(LogbookEntry)
class LogbookEntryAdmin(admin.ModelAdmin):
    list_display = ('placement', 'date', 'created_at')
    list_filter = ('date', 'placement__organization')
    search_fields = ('placement__student__user__username', 'activity_description')

@admin.register(SupervisionComment)
class SupervisionCommentAdmin(admin.ModelAdmin):
    list_display = ('placement', 'supervisor_user', 'week_number', 'date_added')