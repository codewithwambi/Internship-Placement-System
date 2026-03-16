from django.contrib import admin
from .models import InternshipApplication

@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'organization', 'application_date', 'status')
    list_filter = ('status', 'organization')
    search_fields = ('student__user__username', 'organization__name')
    actions = ['approve_applications']

    def approve_applications(self, request, queryset):
        queryset.update(status='approved')
    approve_applications.short_description = "Mark selected applications as Approved"