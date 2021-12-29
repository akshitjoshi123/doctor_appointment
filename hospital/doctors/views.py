from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from appointments.models import Appointment
from rest_auth.registration.views import RegisterView
from rest_framework import generics, serializers
from rest_framework import permissions
from rest_framework.views import APIView
from accounts.models import Specialist, User
from doctors.serializers import InviteDoctorSerializer, DoctorSerializer, DoctorListserializer, AppointmentListSerializer, ConfirmRejectPatientAppointment, UpdateDoctorProfile, ReScheduleAppointment
from rest_framework.permissions import IsAdminUser
from doctors.models import InviteDoctor
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class DoctorRegistration(RegisterView):
    # permission_classes = (IsSuperUser,) 
    serializer_class = DoctorSerializer

class InviteDoctorView(generics.CreateAPIView):
    permission_classes = (IsSuperUser,)
    queryset = InviteDoctor.objects.all()
    serializer_class = InviteDoctorSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        data = serializer.save()
        email_send_to = data.invite_email
        email = EmailMessage('Invitation of Hospital Appointment', 'Registration :- http://127.0.0.1:8000/doctors/register_doctor/', to=[email_send_to])
        email.send()
    

class DoctorList(generics.ListAPIView):
    serializer_class = DoctorListserializer

    def get_queryset(self):
        return User.objects.exclude(specialist = None)


class UpdateDoctorProfileView(LoginRequiredMixin, generics.RetrieveUpdateAPIView):
    serializer_class = UpdateDoctorProfile

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)


class PatientsAppointmentList(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = AppointmentListSerializer

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user)


class ActionAppointmentList(LoginRequiredMixin, generics.RetrieveUpdateAPIView):
    serializer_class = ConfirmRejectPatientAppointment

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user)

    def put(self, request, *args, **kwargs):
        data = self.update(request, *args, **kwargs)
        patient_record = Appointment.objects.filter(id=self.kwargs['pk']).first()
        email_send_to = patient_record.patient.email
        context = {'doctor_name': self.request.user,
                'date': patient_record.date_time,
                'status': patient_record.status}
        body = render_to_string('appointment_action.txt', context)
        email = EmailMessage('Appointment', body , to=[email_send_to])
        email.send()
        return data
        # return self.update(request, *args, **kwargs)


class ReScheduleAppointmentList(LoginRequiredMixin, generics.RetrieveUpdateAPIView):
    serializer_class = ReScheduleAppointment

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user)

    def put(self, request, *args, **kwargs):
        data = self.update(request, *args, **kwargs)
        patient_record = Appointment.objects.filter(id=self.kwargs['pk']).first()
        email_send_to = patient_record.patient.email
        context = {'doctor_name': self.request.user,
                'date': patient_record.date_time}
        body = render_to_string('appointment_reschedule.txt', context)
        email = EmailMessage('Appointment', body , to=[email_send_to])
        email.send()
        return data