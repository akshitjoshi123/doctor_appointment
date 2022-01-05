from datetime import datetime, timedelta
from django.db.models import fields
from rest_framework import serializers
from appointments.models import Appointment
from accounts.models import User
from appointments.constants import FUTURE_DATE_VALIDATION, APPOINTMENTS_8_TO_22

FUTURE_DATE_VALIDATION = FUTURE_DATE_VALIDATION
APPOINTMENTS_8_TO_22 = APPOINTMENTS_8_TO_22


FUTURE_DATE_VALIDATION = FUTURE_DATE_VALIDATION
class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the booking the appointments.
    """
    doctor = serializers.PrimaryKeyRelatedField(queryset= User.objects.exclude(specialist = None))
    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'description']

    def validate_date_time(self, data):
        today = datetime.now()
        if (data.timestamp() <= today.timestamp()):
            raise serializers.ValidationError(FUTURE_DATE_VALIDATION)

        time1 = "8:00:00"
        time2 = "22:00:00"
        my_datetime = datetime.strptime(time1, "%H:%M:%S")
        my_datetime2 = datetime.strptime(time2, "%H:%M:%S")
        my_datetime = data.replace(hour=my_datetime.time().hour, minute=my_datetime.time().minute, second=my_datetime.time().second, microsecond=0)
        my_datetime2 = data.replace(hour=my_datetime2.time().hour, minute=my_datetime2.time().minute, second=my_datetime2.time().second, microsecond=0)
        if my_datetime.time() >= data.time() or my_datetime2.time() <= data.time():
            raise serializers.ValidationError(APPOINTMENTS_8_TO_22)
        return data


class DateWiseAppointment(serializers.Serializer):
    """
    Serializer for list out appointment time for any particular date. 
    """
    selected_date = serializers.DateField()
    doctor_name = serializers.PrimaryKeyRelatedField(queryset= User.objects.exclude(specialist = None))
