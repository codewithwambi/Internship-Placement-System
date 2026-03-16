from django.contrib import admin
from .models import FinalReport, FinalGrade

@admin.register(FinalReport)
class FinalReportAdmin(admin.ModelAdmin):
    # This helps you see at a glance who has submitted their report
    list_display = ('placement', 'submission_date', 'report_file')
    list_filter = ('submission_date', 'placement__organization')
    search_fields = ('placement__student__user__username', 'student_remarks')

@admin.register(FinalGrade)
class FinalGradeAdmin(admin.ModelAdmin):
    # This shows the scores and the calculated total
    list_display = ('placement', 'academic_score', 'workplace_score', 'total_score', 'graded_at')
    list_filter = ('graded_at',)
    search_fields = ('placement__student__user__username',)
    
    # We make 'total_score' read-only since it's a calculated property in the model
    readonly_fields = ('total_score',)

    # Optional: Organizing fields in the detail view
    fieldsets = (
        ('Student Info', {
            'fields': ('placement',)
        }),
        ('Scoring', {
            'fields': ('academic_score', 'workplace_score', 'total_score')
        }),
        ('Feedback', {
            'fields': ('final_remarks',)
        }),
    )