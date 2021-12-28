from django.urls import path, include
from patients.views import PatientsList
from django.conf.urls import url
urlpatterns = [
    path('list_patients/', PatientsList.as_view(), name='list_patients'),
]