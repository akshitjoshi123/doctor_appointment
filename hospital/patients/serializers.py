from rest_framework import serializers
# from allauth.account.adapter import get_adapter
from accounts.models import User



class PatientsListserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'contact', 'email', 'dob']