from django.contrib import admin
from .models import InternshipApplication

@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'organization', 'application_date', 'status')
    list_filter = ('status', 'organization', 'application_date')
    search_fields = ('student__user__username', 'organization__name')
    actions = ['approve_applications']

    def approve_applications(self, request, queryset):
        # We loop through so that each instance is saved individually.
        # This ensures that any signals (like creating a Placement) are triggered.
        for application in queryset:
            application.status = 'approved'
            application.save()
            
    approve_applications.short_description = "Approve selected applications and create placements"