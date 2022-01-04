from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from accounts.models import User
from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from hospital.settings import EMAIL_HOST_USER
