from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from authentication.serializers import UserSerializer


class AuthService:
    @staticmethod
    def authenticate_user(email, password):
        user = authenticate(email=email, password=password)
        if not user:
            return None
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        return user

    @staticmethod
    def generate_tokens(user, data):
        token_serializer = TokenObtainPairSerializer(data=data)
        token_serializer.is_valid(raise_exception=True)
        tokens = token_serializer.validated_data

        return {
            'access': tokens['access'],
            'refresh': tokens['refresh'],
        }
