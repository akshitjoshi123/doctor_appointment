# Create your tasks here

# from demoapp.models import Widget

from celery import shared_task
from datetime import datetime
from appointments.models import Appointment
from datetime import date
from django.db.models import Q

# @task(name='change_appointment_status')
# def change_appointment_status():
#     pass

@shared_task
def change_appointment_status():
    today = date.today()
    # appoint = Appointment.objects.filter(date_time__date=today, status='ReSchedule').update(status='Cancel')
    appoint = Appointment.objects.filter(date_time__date=today).exclude(status='Confirm').update(status='Cancel')
    return appoint