from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.serializers import UserSerializer


class AuthService:
    @staticmethod
    def login(email, password, data):
        user = authenticate(email=email, password=password)
        if not user:
            return None
        user.last_login = timezone.now()
        user.save()
        token_serializer = TokenObtainPairSerializer(data=data)
        token_serializer.is_valid(raise_exception=True)
        tokens = token_serializer.validated_data

        access_token_expiry = timezone.now() + \
            timedelta(
                seconds=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
        refresh_token_expiry = timezone.now() + \
            timedelta(
                seconds=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())

        return {
            'user': UserSerializer(user).data,
            'tokens': {
                'AccessToken': tokens['access'],
                'AccessTokenExpiry': access_token_expiry.isoformat(),
                'RefreshToken': {
                    'token': tokens['refresh'],
                    'expiry': refresh_token_expiry.isoformat()
                }
            }
        }
