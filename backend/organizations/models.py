from django.db import models
from users.models import WorkplaceSupervisor ,Student, AcademicSupervisor


class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
  #  location = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    contact_email = models.EmailField(blank=True, null=True)
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Department(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,related_name='departments')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.organization.name})"

class OrganizationSupervisor(models.Model):
    supervisor = models.OneToOneField(
        WorkplaceSupervisor, 
        on_delete=models.CASCADE, 
        related_name='assignment'
    )
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        related_name='staff'
    )
    department = models.ForeignKey(
        Department, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.supervisor.user.get_full_name()} at {self.organization.name}"
    

  

class Placement(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='placement')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='placements')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Linking both supervisors to the student's internship
    workplace_supervisor = models.ForeignKey(OrganizationSupervisor, on_delete=models.SET_NULL, null=True, blank=True)
    academic_supervisor = models.ForeignKey(AcademicSupervisor, on_delete=models.SET_NULL, null=True, blank=True)

    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.student.user.username} - {self.organization.name}"