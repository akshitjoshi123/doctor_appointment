from django.shortcuts import render
from rest_framework import generics
from appointments.serializers import AppointmentSerializer, DateWiseAppointment
from appointments.models import Appointment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from appointments.services import set_appointment_create, get_date_wise_list
import logging

# Create your views here.

class AppointmentCreateApi(LoginRequiredMixin, generics.CreateAPIView):
    """
    View for booking the appointments.
    """
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all() 
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        get_time = serializer.validated_data['date_time']
        get_doctor = serializer.validated_data['doctor']
        try:
            create_appointment = set_appointment_create(self, get_time, get_doctor, serializer)
        except Exception as e:
            logging.error(str(e))


class DateWiseListView(LoginRequiredMixin, APIView):
    """
    View for list out appointment time for any particular date. 
    """
    serializer_class = DateWiseAppointment
    def post(self, request):
        data = []
        try:
            serializers = DateWiseAppointment(data=request.data)
            if serializers.is_valid(raise_exception=True):
                s_date = serializers.validated_data['selected_date']
                d_name = serializers.validated_data['doctor_name']
                data = get_date_wise_list(self, s_date, d_name, data)
            return Response(data)
        except Exception as e:
            logging.error(str(e))
            return Response(data)

                