from django.db import models

# Create your models here.

class InviteDoctor(models.Model):
    invite_email = models.EmailField(max_length=30, null=True, blank=True)

    def __str__(self):
        return str(self.invite_email)
