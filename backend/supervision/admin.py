from django.contrib import admin
from .models import LogbookEntry, SupervisionComment

@admin.register(LogbookEntry)
class LogbookEntryAdmin(admin.ModelAdmin):
    # Added 'is_present' to fulfill the attendance monitoring requirement
    list_display = ('placement', 'date', 'is_present', 'created_at')
    list_filter = ('is_present', 'date', 'placement__organization')
    search_fields = ('placement__student__user__username', 'activity_description')

@admin.register(SupervisionComment)
class SupervisionCommentAdmin(admin.ModelAdmin):
    # Added 'is_private_to_staff' so admins can see which comments are hidden from students
    list_display = ('placement', 'supervisor_user', 'week_number', 'is_private_to_staff', 'date_added')
    list_filter = ('week_number', 'supervisor_user__role', 'date_added')
    search_fields = ('placement__student__user__username', 'comment')