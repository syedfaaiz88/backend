from rest_framework import serializers

from services.user_service import UserService
from utils.validate_password import validate_password_strength
from .models import User
from django.utils import timezone

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'address', 'date_of_birth', 'gender', 'bio', 'first_name', 'last_name', 'date_joined', 'is_verified']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'phone_number': {'min_length': 7},
        }

    def validate(self, data):
        if data['password']:
            password = data['password']
            validate_password_strength(password)
        if data['date_of_birth'] and data['date_of_birth'].year > timezone.now().year - 6:
            raise serializers.ValidationError(
                {'date_of_birth': 'You must be at least 6 years old.'})
        return data

    def create(self, validated_data):
        user = UserService.create_user(validated_data)
        if not user:
            raise serializers.ValidationError("Failed to create user.", "USER_CREATION_FAILED")
        return user
