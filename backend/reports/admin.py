from django.contrib import admin
from .models import FinalReport, FinalGrade

@admin.register(FinalReport)
class FinalReportAdmin(admin.ModelAdmin):
    list_display = ('placement', 'submission_date', 'report_file')
    list_filter = ('submission_date', 'placement__organization')
    search_fields = ('placement__student__user__username', 'student_remarks')

@admin.register(FinalGrade)
class FinalGradeAdmin(admin.ModelAdmin):
    list_display = ('placement', 'academic_score', 'workplace_score', 'display_total_score', 'graded_at')
    list_filter = ('graded_at',)
    search_fields = ('placement__student__user__username',)
    readonly_fields = ('total_score',)

    # Helper method to display the calculated property in the list view
    def display_total_score(self, obj):
        return obj.total_score
    display_total_score.short_description = 'Total Score'

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