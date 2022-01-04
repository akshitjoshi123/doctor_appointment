from django.urls import path, include
from doctors.views import InviteDoctorView, DoctorRegistration, DoctorList, PatientsAppointmentList, ActionAppointmentList, UpdateDoctorProfileView, ReScheduleAppointmentList, MyPatientProfileView
from django.conf.urls import url
urlpatterns = [
    path('register_doctor/', DoctorRegistration.as_view(), name='register_doctor'),
    path('invite_doctor/', InviteDoctorView.as_view(), name='invite_doctor'),
    path('list_doctor/', DoctorList.as_view(), name='list_doctor'),
    path('list_appointment/', PatientsAppointmentList.as_view(), name='list_appointment'),
    path('action_appointment/<int:pk>/', ActionAppointmentList.as_view(), name='action_appointment'),
    path('update_profile/<int:pk>/', UpdateDoctorProfileView.as_view(), name='update_profile'),
    path('reschedule_appointment/<int:pk>/', ReScheduleAppointmentList.as_view(), name='reschedule_appointment'),
    path('my_patient_profile/', MyPatientProfileView.as_view(), name='my_patient_profile'),
]