from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from rest_framework import generics, serializers
from rest_framework import permissions
from rest_framework.views import APIView
from accounts.models import Specialist, User
from doctors.serializers import InviteDoctorSerializer, DoctorSerializer, DoctorListserializer
from rest_framework.permissions import IsAdminUser
from doctors.models import InviteDoctor
from django.core.mail import EmailMessage

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
