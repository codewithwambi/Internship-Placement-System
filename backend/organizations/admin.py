from django.contrib import admin
from .models import Organization, Department, OrganizationSupervisor, Placement

class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    # Added address and contact_email to match your 'Organization' entity attributes
    list_display = ('name', 'industry', 'address', 'contact_email') 
    search_fields = ('name', 'industry', 'address')
    inlines = [DepartmentInline]

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')
    list_filter = ('organization',)

@admin.register(OrganizationSupervisor)
class OrganizationSupervisorAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'organization', 'department')
    list_filter = ('organization', 'department')
    search_fields = ('supervisor__user__username', 'organization__name')

    def get_username(self, obj):
        return obj.supervisor.user.get_full_name() or obj.supervisor.user.username
    get_username.short_description = 'Supervisor Name'

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    # Status and dates are critical for your 'Workflow States'
    list_display = ('student', 'organization', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'organization', 'start_date')
    search_fields = ('student__user__username', 'organization__name')
    
    # Organizing the placement details into sections for the Admin
    fieldsets = (
        ('Placement info', {
            'fields': ('student', 'organization', 'department', 'status')
        }),
        ('Supervision', {
            'fields': ('workplace_supervisor', 'academic_supervisor')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
    )