from django.shortcuts import render
from rest_framework import generics
from appointments.serializers import AppointmentSerializer
from appointments.models import Appointment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.

class AppointmentCreateApi(LoginRequiredMixin, generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all() 
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        data = serializer.save(patient=self.request.user)
        email_send_to = data.doctor.email
        context = {'name': data.patient.first_name,
                'date': data.date_time}
        body = render_to_string('appointment_book.txt', context)
        email = EmailMessage('New Appointment', body , to=[email_send_to])
        email.send()