from django.shortcuts import render
from rest_framework import generics
from appointments.serializers import AppointmentSerializer, DateWiseAppointment
from appointments.models import Appointment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from datetime import datetime, time, timedelta
from appointments.constants import APPOINTMENT_VALIDATION

APPOINTMENT_VALIDATION = APPOINTMENT_VALIDATION


def set_appointment_create(self, get_time, get_doctor, serializer, *args, **kwargs):
    appointment_time = Appointment.objects.filter(doctor=get_doctor)
    for i in appointment_time:
        if (i.date_time + timedelta(minutes = -15)) <= get_time <= (i.date_time + timedelta(minutes = 30)):
            raise serializers.ValidationError(APPOINTMENT_VALIDATION)

    data = serializer.save(patient=self.request.user)
    email_send_to = data.doctor.email
    context = {'name': data.patient.first_name,
                'date': data.date_time}
    body = render_to_string('appointment_book.txt', context)
    email = EmailMessage('New Appointment', body , to=[email_send_to])
    email.send()


def get_date_wise_list(self, s_date, d_name, data, *args, **kwargs):
    appointment_date = Appointment.objects.filter(date_time__date=s_date, doctor=d_name).order_by("date_time")
    for i in appointment_date:
        time = i.date_time.time(), (i.date_time + timedelta(minutes = 30)).time()
        data.append(time)
    return data