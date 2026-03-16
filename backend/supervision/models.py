from django.db import models
from organizations.models import Placement

class LogbookEntry(models.Model):
    placement = models.ForeignKey(Placement, on_delete=models.CASCADE, related_name='logbook_entries')
    date = models.DateField()
    activity_description = models.TextField(help_text="Describe the tasks performed today.")
    skills_learned = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Logbook Entries"
        ordering = ['-date'] # Show newest entries first

    def __str__(self):
        return f"Entry for {self.date} - {self.placement.student.user.username}"

class SupervisionComment(models.Model):
    # This allows both Academic and Workplace supervisors to leave feedback
    placement = models.ForeignKey(Placement, on_delete=models.CASCADE, related_name='supervision_comments')
    supervisor_user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comment = models.TextField()
    week_number = models.PositiveIntegerField(help_text="Which week of the internship is this for?")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.supervisor_user.username} for Week {self.week_number}"