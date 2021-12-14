from django.urls import path, include
from rest_auth.views import PasswordResetView
urlpatterns = [
    path('', include('rest_auth.urls')),
    # path('password_reset/', include('django_rest_passwordreset.urls')),
    path('registration/', include('rest_auth.registration.urls')),
]