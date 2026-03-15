from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, AcademicSupervisor, WorkplaceSupervisor

# We are going to unregister the default Group model just to see if the admin refreshes
# admin.site.unregister(Group) # Optional: only if you want to hide Groups

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    # This tells Django exactly where to put our custom fields in the edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('role', 'phone')}),
    )

admin.site.register(Student)
admin.site.register(AcademicSupervisor)
admin.site.register(WorkplaceSupervisor)