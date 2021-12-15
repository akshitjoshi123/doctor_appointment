from django.db.models import fields
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
# from allauth.account.adapter import get_adapter
from accounts.models import Specialist, User
from rest_auth.serializers import PasswordChangeSerializer, PasswordResetConfirmSerializer


class UserSerializer(RegisterSerializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    contact = serializers.CharField()
    dob = serializers.DateField()
    password1 = serializers.CharField(
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'}
    )

    
    def save(self, request):

        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.contact = self.data.get('contact')
        user.dob = self.data.get('dob')
        user.save()
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'contact',
            'dob',
        )
        read_only_fields = ('pk', 'username', 'dob')


class CustomPasswordChange(PasswordChangeSerializer):
    new_password1 = serializers.CharField(
        style={'input_type': 'password'}
    )
    new_password2 = serializers.CharField(
        style={'input_type': 'password'}
    )


class CustomPasswordResetConfirm(PasswordResetConfirmSerializer):
    new_password1 = serializers.CharField(
        style={'input_type': 'password'}
    )
    new_password2 = serializers.CharField(
        style={'input_type': 'password'}
    )