from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
# from allauth.account.adapter import get_adapter
from accounts.models import Specialist, User
from doctors.models import InviteDoctor


class DoctorSerializer(RegisterSerializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    contact = serializers.CharField()
    dob = serializers.DateField()
    password1 = serializers.CharField(
        style={'input_type': 'password'},
        write_only = True
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only = True
    )
    specialist = serializers.ChoiceField(choices=Specialist)
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.contact = self.data.get('contact')
        user.dob = self.data.get('dob')
        user.specialist = self.data.get('specialist')
        user.save()  
        return user


class InviteDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteDoctor
        fields = ['invite_email']


class DoctorListserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'contact', 'email', 'specialist']
