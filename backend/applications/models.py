from django.db import models
from users.models import Student
from organizations.models import Organization


def student_cv_path(instance, filename):
    # This saves the file to: media/cvs/username/filename
    return f'cvs/{instance.student.user.username}/{filename}'


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
    cv_file = models.FileField(upload_to=student_cv_path, blank=True, null=True)

    preferred_department = models.CharField(max_length=100, blank=True, null=True)
  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    class Meta:
        # This ensures the newest applications appear first in the admin dashboard
        ordering = ['-application_date']

    def __str__(self):
        return f"{self.student.user.username} - {self.organization.name} ({self.status})"
    

