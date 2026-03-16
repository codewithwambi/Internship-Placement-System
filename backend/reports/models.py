from django.db import models
from organizations.models import Placement

class FinalReport(models.Model):
    placement = models.OneToOneField(Placement, on_delete=models.CASCADE, related_name='final_report')
    report_file = models.FileField(upload_to='reports/final/')
    submission_date = models.DateTimeField(auto_now_add=True)
    student_remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Final Report - {self.placement.student.user.username}"

class FinalGrade(models.Model):
    placement = models.OneToOneField(Placement, on_delete=models.CASCADE, related_name='final_grade')
    academic_score = models.DecimalField(max_digits=5, decimal_places=2) # e.g., 85.50
    workplace_score = models.DecimalField(max_digits=5, decimal_places=2)
    final_remarks = models.TextField()
    graded_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_score(self):
        return (self.academic_score + self.workplace_score) / 2

    def __str__(self):
        return f"Grade for {self.placement.student.user.username}: {self.total_score}"