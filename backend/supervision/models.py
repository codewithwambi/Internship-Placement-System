from django.db import models
from organizations.models import Placement
from django.conf import settings

class LogbookEntry(models.Model):
    placement = models.ForeignKey(Placement, on_delete=models.CASCADE, related_name='logbook_entries')
    date = models.DateField()
    activity_description = models.TextField(help_text="Describe the tasks performed today.")
    skills_learned = models.TextField(blank=True, null=True)

    # New field: Satisfies the 'Attendance Tracking' requirement
    is_present = models.BooleanField(default=True, verbose_name="Attended Work")
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Logbook Entries"
        ordering = ['-date'] # Show newest entries first

    def __str__(self):
        return f"Entry for {self.date} - {self.placement.student.user.username}"

class SupervisionComment(models.Model):
    placement = models.ForeignKey(Placement, on_delete=models.CASCADE, related_name='supervision_comments')
    # Using settings.AUTH_USER_MODEL is more robust for foreign keys to User
    supervisor_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    comment = models.TextField()
    week_number = models.PositiveIntegerField(help_text="Which week of the internship is this for?")
    
    # New field: Helps frontend filter workplace vs academic feedback
    is_private_to_staff = models.BooleanField(default=False, help_text="If true, student cannot see this.")
    
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.supervisor_user.get_full_name()} for Week {self.week_number}"