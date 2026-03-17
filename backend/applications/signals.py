from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InternshipApplication
from organizations.models import Placement
from datetime import date, timedelta

@receiver(post_save, sender=InternshipApplication)
def create_placement_on_approval(sender, instance, created, **kwargs):
    # Only act if the status was just changed to 'approved'
    if instance.status == 'approved':
        
        # IMPROVED CHECK: Only prevent creation if an ACTIVE placement already exists
        active_placement_exists = Placement.objects.filter(
            student=instance.student, 
            status='active'
        ).exists()
        
        if not active_placement_exists:
            Placement.objects.create(
                student=instance.student,
                organization=instance.organization,
                # Default dates: starts today, ends in 90 days
                start_date=date.today(),
                end_date=date.today() + timedelta(days=90),
                status='active'
            )