import uuid
from django.db import models
from account.models import User  # Import the User model from the account app

class MaintenanceProvider(models.Model):
    HVAC = 'hvac'
    ELEVATORS = 'elevators'
    GENERATORS = 'generators'

    SPECIALIZATION_CHOICES = [
        (HVAC, 'HVAC Systems'),
        (ELEVATORS, 'Elevators'),
        (GENERATORS, 'Generators'),
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4),
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES, default=HVAC)
    company_name = models.CharField(max_length=255, null=False, blank=False)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    company_registration_number = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f"{self.company_name} ({self.specialization})"

