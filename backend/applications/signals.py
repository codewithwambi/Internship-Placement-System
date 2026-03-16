from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InternshipApplication
from organizations.models import Placement
from datetime import date, timedelta

@receiver(post_save, sender=InternshipApplication)
def create_placement_on_approval(sender, instance, created, **kwargs):
    # We only act if the status was just changed to 'approved'
    # and if a placement doesn't already exist for this student
    if instance.status == 'approved':
        placement_exists = Placement.objects.filter(student=instance.student).exists()
        
        if not placement_exists:
            Placement.objects.create(
                student=instance.student,
                organization=instance.organization,
                # We set some default dates (e.g., starts today, ends in 3 months)
                # The admin can change these later in the dashboard
                start_date=date.today(),
                end_date=date.today() + timedelta(days=90),
                status='active'
            )