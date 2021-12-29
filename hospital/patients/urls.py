from django.urls import path, include
from patients.views import PatientsList, ReScheduledAppointmentList
from django.conf.urls import url
urlpatterns = [
    path('list_patients/', PatientsList.as_view(), name='list_patients'),
    path('reschedule/<int:pk>/', ReScheduledAppointmentList.as_view(), name='reschedule'),
]