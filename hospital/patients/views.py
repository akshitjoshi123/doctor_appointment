from django.shortcuts import render
from rest_framework import generics
from accounts.models import Specialist, User
from appointments.models import Appointment
from patients.serializers import PatientsListserializer, ConfirmRejectReScheduleAppointment
from rest_framework.permissions import IsAdminUser
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class PatientsList(generics.ListAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = PatientsListserializer

    def get_queryset(self):
        return User.objects.filter(specialist = None)


class ReScheduledAppointmentList(LoginRequiredMixin, generics.RetrieveUpdateAPIView):
    serializer_class = ConfirmRejectReScheduleAppointment

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user)

    def put(self, request, *args, **kwargs):
        data = self.update(request, *args, **kwargs)
        doctor_record = Appointment.objects.filter(id=self.kwargs['pk']).first()
        email_send_to = doctor_record.doctor.email
        context = {'patient_name': self.request.user,
                'date': doctor_record.date_time,
                'status': doctor_record.status}
        body = render_to_string('patient_reschedule.txt', context)
        email = EmailMessage('Appointment', body , to=[email_send_to])
        email.send()
        return data


