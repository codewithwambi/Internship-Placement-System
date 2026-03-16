from django.db import models
from users.models import Student
from organizations.models import Organization

class InternshipApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField(blank=True, null=True)
    cv_link = models.URLField(max_length=500, blank=True, null=True) # Or use FileField later
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    def __str__(self):
        return f"{self.student.user.username} - {self.organization.name} ({self.status})"