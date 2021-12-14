from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

Specialist = (
    ("Orthopedics", "Orthopedics"),
    ("Gynecology", "Gynecology"),
    ("General_Surgen", "General_Surgen"),
    ("Pathology", "Pathology"),
)

class User(AbstractUser):
    """Abstract user table"""   

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(null=True)
    specialist = models.CharField(max_length=30, choices=Specialist, null=True, blank=True)

    def __str__(self):
        return str(self.first_name)
