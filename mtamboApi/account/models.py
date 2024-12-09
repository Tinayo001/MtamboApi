from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

# Enum for account types
class AccountType(models.TextChoices):
    DEVELOPER = 'developer', 'Developer'
    MAINTENANCE = 'maintenance_company', 'Maintenance_Company'
    TECHNICIAN = 'technician', 'Technician'

# Custom user model extending AbstractUser
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    account_type = models.CharField(
        max_length=50,
        choices=AccountType.choices,
        default=AccountType.DEVELOPER,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_username(self):
        """
        Generate a unique username based on the user's first and last names.
        If the username already exists, append a counter to ensure uniqueness.
        """
        base_username = f"{self.first_name.lower()} {self.last_name.lower()}"
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        return username

    def save(self, *args, **kwargs):
        """
        Automatically generate a username if it is not set before saving.
        """
        if not self.username:
            self.username = self.generate_username()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.account_type})"


