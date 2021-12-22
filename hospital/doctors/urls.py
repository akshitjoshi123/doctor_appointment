from django.urls import path, include
from doctors.views import InviteDoctorView, DoctorRegistration, DoctorList
from django.conf.urls import url
urlpatterns = [
    # path('password_reset/', include('django_rest_passwordreset.urls')),
    path('register_doctor/', DoctorRegistration.as_view(), name='register_doctor'),
    path('invite_doctor/', InviteDoctorView.as_view(), name='invite_doctor'),
    path('list_doctor/', DoctorList.as_view(), name='list_doctor'),
    url(r'invite/', include('drf_simple_invite.urls', namespace='drf_simple_invite')),
]