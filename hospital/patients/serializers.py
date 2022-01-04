from rest_framework import serializers
from accounts.models import User
from appointments.models import Appointment, status


class PatientsListserializer(serializers.ModelSerializer):
    """
    Serializer for show the details of patients.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'contact', 'email', 'dob']


class ConfirmRejectReScheduleAppointment(serializers.ModelSerializer):
    """
    Serializer for take action on the rescheduling appointment.
    """
    doctor_name = serializers.CharField(source='full_name_doctor', read_only=True)
    status = serializers.ChoiceField(choices = status[0:2])

    class Meta:
        model = Appointment
        fields = ['doctor_name', 'date_time', 'status', 'description']
        read_only_fields = ('date_time', 'description')
