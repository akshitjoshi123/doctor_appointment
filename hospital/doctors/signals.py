from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from accounts.models import User
from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from hospital.settings import EMAIL_HOST_USER


# @receiver(post_save, sender=User)
# def send_mail_on_create(sender, instance, **kwargs):
#     if kwargs['created']:
#         send_mail(
#             'Hospital: Registration',
#             'Congrats!! You are register,Your Email address is Login Password. NOTE: Once you login then Reset Your password',
#             EMAIL_HOST_USER,
#             [instance.email],
#         )
        