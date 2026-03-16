from django.contrib import admin
from .models import Organization, Department, OrganizationSupervisor,Placement

# This allows you to add Departments directly while looking at an Organization
class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'industry')
    search_fields = ('name', 'industry', 'location')
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

    # Helper method to show the username in the list view
    def get_username(self, obj):
        return obj.supervisor.user.username
    get_username.short_description = 'Supervisor Name'


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('student', 'organization', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'organization')
    search_fields = ('student__user__username', 'organization__name')    