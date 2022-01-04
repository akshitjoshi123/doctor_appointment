from django.db import models
from django.db.models import fields
from django.db.models.enums import Choices
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
# from allauth.account.adapter import get_adapter
from accounts.models import Specialist, User
from doctors.models import InviteDoctor
from appointments.models import Appointment, status


class DoctorSerializer(RegisterSerializer):
    """
    Serializer for doctor registration.
    """
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    contact = serializers.CharField()
    dob = serializers.DateField()
    password1 = serializers.CharField(
        style={'input_type': 'password'},
        write_only = True
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only = True
    )
    specialist = serializers.ChoiceField(choices=Specialist)
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.contact = self.data.get('contact')
        user.dob = self.data.get('dob')
        user.specialist = self.data.get('specialist')
        user.save()  
        return user


class InviteDoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for doctor invitation.
    """
    class Meta:
        model = InviteDoctor
        fields = ['invite_email']


class DoctorListserializer(serializers.ModelSerializer):
    """
    Serializer for list out doctor deatils.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'contact', 'email', 'specialist']


class UpdateDoctorProfile(serializers.ModelSerializer):
    """
    Serializer for update profile for doctor.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'contact', 'email', 'dob', 'specialist']


class AppointmentListSerializer(serializers.ModelSerializer):
    """
    Serializer for list out appointments
    """
    patient_name = serializers.CharField(source='full_name')

    class Meta:
        model = Appointment
        fields = ['patient_name', 'date_time', 'status', 'description']


class ConfirmRejectPatientAppointment(serializers.ModelSerializer):
    """
    Serializers for action command(Confirm or cancel the appointment).
    """
    patient_name = serializers.CharField(source='full_name', read_only=True)
    status = serializers.ChoiceField(choices = status[0:2])

    class Meta:
        model = Appointment
        fields = ['patient_name', 'date_time', 'status', 'description']
        read_only_fields = ('date_time', 'description')


class ReScheduleAppointment(serializers.ModelSerializer):
    """
    Serializer for Re-Schedule the appointments.
    """
    patient_name = serializers.CharField(source='full_name', read_only=True)
    status = serializers.ChoiceField(choices=status[2])

    class Meta:
        model = Appointment
        fields = ['patient_name', 'date_time', 'status', 'description']
        read_only_fields = ('description',)


class MyPatientProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for showing the profile of patients for doctor only.
    """
    user_name = serializers.CharField(source='patient.username', read_only=True)
    first_name = serializers.CharField(source='patient.first_name', read_only=True)
    last_name = serializers.CharField(source='patient.last_name', read_only=True)
    email = serializers.EmailField(source='patient.email', read_only=True)
    contact = serializers.CharField(source='patient.contact', read_only=True)
    dob = serializers.DateField(source='patient.dob', read_only=True)

    class Meta:
        model = User
        fields = ['user_name', 'first_name', 'last_name', 'email', 'contact', 'dob']