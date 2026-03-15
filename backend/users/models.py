from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    """
    Custom User model to handle different roles within the 
    Internship Placement System.
    """
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        ACADEMIC_SUPERVISOR = "ACADEMIC_SUPERVISOR", "Academic Supervisor"
        WORKPLACE_SUPERVISOR = "WORKPLACE_SUPERVISOR", "Workplace Supervisor"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.ADMIN
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    # We use the built-in 'first_name', 'last_name', and 'email' from AbstractUser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    registration_number = models.CharField(max_length=50, unique=True)
    course = models.CharField(max_length=100)

    def __str__(self):
        return f"Student: {self.user.get_full_name()} - {self.registration_number}"


class AcademicSupervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"Academic Sup: {self.user.get_full_name()}"


class WorkplaceSupervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Workplace Sup: {self.user.get_full_name()} ({self.company_name})"
    


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.Role.STUDENT:
            Student.objects.get_or_create(user=instance)
        elif instance.role == User.Role.ACADEMIC_SUPERVISOR:
            AcademicSupervisor.objects.get_or_create(user=instance)
        elif instance.role == User.Role.WORKPLACE_SUPERVISOR:
            WorkplaceSupervisor.objects.get_or_create(user=instance)    