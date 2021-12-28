from django.shortcuts import render
from rest_framework import generics
from accounts.models import Specialist, User
from patients.serializers import PatientsListserializer
from rest_framework.permissions import IsAdminUser

# Create your views here.

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class PatientsList(generics.ListAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = PatientsListserializer

    def get_queryset(self):
        return User.objects.filter(specialist = None)


