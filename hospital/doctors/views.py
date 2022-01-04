from django.contrib.auth.mixins import LoginRequiredMixin
from rest_auth.registration.views import RegisterView
from rest_framework import generics
from accounts.models import Specialist, User
from doctors.serializers import InviteDoctorSerializer, DoctorSerializer, DoctorListserializer, AppointmentListSerializer, ConfirmRejectPatientAppointment, UpdateDoctorProfile, ReScheduleAppointment, MyPatientProfileSerializer
from rest_framework.permissions import IsAdminUser
from doctors.models import InviteDoctor
from doctors.services import InviteDoctorManager, DoctorManager, ActionAppointment, RescheduleAppointment, MyPatientProfile
# Create your views here.

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class DoctorRegistration(RegisterView):
    """
    View for doctor registration.
    """
    serializer_class = DoctorSerializer


class InviteDoctorView(generics.CreateAPIView):
    """
    View for Invite Doctor for using system.
    """
    permission_classes = (IsSuperUser,)
    queryset = InviteDoctor.objects.all()
    serializer_class = InviteDoctorSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        data = serializer.save()
        invite_doctor = InviteDoctorManager.set_invite_doctor(self, data)


class DoctorList(generics.ListAPIView):
    """
    This View is use to list the doctor details.
    """
    serializer_class = DoctorListserializer

    def get_queryset(self):
        return DoctorManager.get_doctor_list(self)


class UpdateDoctorProfileView(LoginRequiredMixin, generics.RetrieveUpdateAPIView):
    """
    View for update the profile of doctor by its self.
    """
    serializer_class = UpdateDoctorProfile

    def get_queryset(self):
        return DoctorManager.set_update_doctor_profile(self)


class PatientsAppointmentList(LoginRequiredMixin, generics.ListAPIView):
    """
    View for list out the appointment for any particular doctor. 
    """
    serializer_class = AppointmentListSerializer

    def get_queryset(self):
        return ActionAppointment.get_appointment(self)


class ActionAppointmentList(LoginRequiredMixin, generics.RetrieveUpdateAPIView):
    """
    View for take action on the appointment(Doctor can Confirm or cancel the appointment).
    """
    serializer_class = ConfirmRejectPatientAppointment

    def get_queryset(self):
        return ActionAppointment.get_appointment(self)

    def put(self, request, *args, **kwargs):
        data = self.update(request, *args, **kwargs)
        action = ActionAppointment.set_action(self)
        return data


class ReScheduleAppointmentList(LoginRequiredMixin, generics.RetrieveUpdateAPIView):
    """
    View for rescheduling the appointments.
    """
    serializer_class = ReScheduleAppointment

    def get_queryset(self):
        return ActionAppointment.get_appointment(self)

    def put(self, request, *args, **kwargs):
        data = self.update(request, *args, **kwargs)
        reschedule = RescheduleAppointment.set_reschedule(self) 
        return data


class MyPatientProfileView(LoginRequiredMixin, generics.ListAPIView):
    """
    View for show the patients profile by its Doctor
    """
    serializer_class = MyPatientProfileSerializer

    def get_queryset(self):
        return MyPatientProfile.get_profile(self)