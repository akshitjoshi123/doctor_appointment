from rest_framework import generics
from accounts.models import Specialist
from patients.serializers import PatientsListserializer, ConfirmRejectReScheduleAppointment
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.mixins import LoginRequiredMixin
from patients.services import PatientsManager, ReSheduleManager

# Create your views here.

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class PatientsList(generics.ListAPIView):
    """
    View for display the details of patients.
    """
    permission_classes = (IsSuperUser,)
    serializer_class = PatientsListserializer

    def get_queryset(self):
        return PatientsManager.get_patients(self)


class ReScheduledAppointmentList(LoginRequiredMixin, generics.RetrieveUpdateAPIView):
    """
    View for take action on rescheduling appointments.
    """
    serializer_class = ConfirmRejectReScheduleAppointment

    def get_queryset(self):
        return ReSheduleManager.get_patients(self)

    def put(self, request, *args, **kwargs):
        data = self.update(request, *args, **kwargs)
        mail_sent = ReSheduleManager.set_reschedule(self)
        return data


