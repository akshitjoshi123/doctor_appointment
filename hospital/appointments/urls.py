from django.urls import path, include
from appointments.views import AppointmentCreateApi, DateWiseListView
from django.conf.urls import url
urlpatterns = [
    path('book_appointment/', AppointmentCreateApi.as_view(), name='book_appointment'),
    path('date_wise/', DateWiseListView.as_view(), name='date_wise'),
]