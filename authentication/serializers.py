from rest_framework import serializers
from authentication.services.user_service import UserService
from .models import User
from django.utils import timezone
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'address', 'date_of_birth', 'gender', 'bio', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }

    def validate(self, data):
        if data['password']:
            password = data['password']
            if len(password) < 8 or not any(char.isupper() for char in password) or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in password):
                raise serializers.ValidationError(
                    {'password': 'Password must be at least 8 characters long, contain one uppercase letter and one special character.'})
        if data['date_of_birth'] and data['date_of_birth'].year > timezone.now().year - 6:
            raise serializers.ValidationError(
                {'dob': 'You must be at least 6 years old.'})
        return data

    def create(self, validated_data):
        user = UserService.create_user(validated_data)
        if not user:
            raise serializers.ValidationError("Failed to create user.", "USER_CREATION_FAILED")
        return user
