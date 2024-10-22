from rest_framework import serializers
from django.core.validators import RegexValidator
from services.user_service import UserService
from utils.validate_password import validate_password_strength
from .models import User
from django.utils import timezone

class DummySerializer(serializers.Serializer):
    pass

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'address', 'date_of_birth', 'gender', 'bio', 'first_name', 'last_name', 'date_joined', 'is_verified', 'profile_picture']
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

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    again_new_password = serializers.CharField()

    def validate_old_password(self, value):
        validate_password_strength(value)
        return value
    
    def validate_new_password(self, value):
        validate_password_strength(value)
        return value

    def validate_again_new_password(self, value):
        validate_password_strength(value)
        return value
    
class EditProfileDetailsSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    user_name = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)

class EditProfilePictureSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField()

class UserNameAvailablilitySerializer(serializers.Serializer):
    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9.]+$',
        message="Username must contain only letters, numbers, and dots (.)"
    )
    username = serializers.CharField(min_length=5,validators=[username_validator])

    def validate_username(self, value):
        # Check if the username starts or ends with a dot
        if value.startswith('.') or value.endswith('.'):
            raise serializers.ValidationError("Contains misplaced special characters")
        return value
