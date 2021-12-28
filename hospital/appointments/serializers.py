from rest_framework import serializers
from appointments.models import Appointment
from accounts.models import User

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset= User.objects.exclude(specialist = None))
    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'description']
