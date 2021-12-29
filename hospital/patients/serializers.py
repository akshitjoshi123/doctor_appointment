from rest_framework import serializers
# from allauth.account.adapter import get_adapter
from accounts.models import User
from appointments.models import Appointment, action_status



class PatientsListserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'contact', 'email', 'dob']


class ConfirmRejectReScheduleAppointment(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='full_name_doctor', read_only=True)
    status = serializers.ChoiceField(choices = action_status)
    print(doctor_name)

    class Meta:
        model = Appointment
        fields = ['doctor_name', 'date_time', 'status', 'description']
        read_only_fields = ('date_time', 'description')
