from django.db import models

from accounts.models import User

# Create your models here.

status = (
    ("Confirm", "Confirm"),
    ("Cancel", "Cancel"),
    ("ReSchedule", "ReSchedule"),
    ("Pending", "Pending"),
)


class Appointment(models.Model):
    """
    Table of appointment details with status
    """
    patient = models.ForeignKey(User, related_name="patient", on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name="doctor", on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=status, default="Pending")
    description = models.TextField(max_length=200)

    def doctor_name(self):
        return User.objects.exclude(specialist = None)

    def __str__(self):
        return str(self.patient)

    def full_name(self):
        f_name = ""
        f_name += self.patient.first_name if self.patient.first_name else "" 
        f_name += self.patient.last_name if self.patient.last_name else ""
        return f_name

    def full_name_doctor(self):
        f_name = ""
        f_name += self.doctor.first_name if self.doctor.first_name else "" 
        f_name += self.doctor.last_name if self.doctor.last_name else ""
        return f_name