from django.urls import path, include
from appointments.views import AppointmentCreateApi
from django.conf.urls import url
urlpatterns = [
    path('book_appointment/', AppointmentCreateApi.as_view(), name='book_appointment'),
]