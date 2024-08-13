from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer, LoginSerializer
from .services.auth_service import AuthService
from .utils import custom_response, send_verification_email
from rest_framework import status
from django.utils import timezone
import uuid 

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        user = serializer.save()
        user.set_password(password)
        user.save()

        # Send verification email
        send_verification_email(user)

        return custom_response(
            status=True,
            message=f"Verification email sent to {user.email}. Please verify your account.",
            result=UserSerializer(user).data,  # Serialize the user object
            has_result=True,
            status_code=status.HTTP_201_CREATED
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Handle validation errors with custom response
            return custom_response(
                status=False,
                message="Validation failed.",
                error_code="VALIDATION_ERROR",
                result=serializer.errors,
                has_result=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        return self.perform_create(serializer)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Handle validation errors with custom response
            return custom_response(
                status=False,
                message="Validation failed.",
                error_code="VALIDATION_ERROR",
                result=serializer.errors,
                has_result=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = AuthService.authenticate_user(email=email, password=password)
        if not user:
            return custom_response(
                status=False,
                message="Invalid credentials.",
                error_code="INVALID_CREDENTIALS",
                has_result=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if not user.is_verified:
            send_verification_email(user)
            return custom_response(
                status=True,
                message=f"Verification email sent to {user.email}. Please verify your account.",
                has_result=False,
                status_code=status.HTTP_201_CREATED
            )

        tokens = AuthService.generate_tokens(user, request.data)
        return custom_response(
            status=True,
            message="Login successful.",
            result={
                'user': UserSerializer(user).data,
                'tokens': tokens
            },
            has_result=True,
            status_code=status.HTTP_200_OK
        )

class VerifyEmailView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, token, *args, **kwargs):
        try:
            uuid.UUID(token)
        except ValueError:
            return custom_response(
                status=False,
                message="Invalid token format.",
                error_code="INVALID_TOKEN_FORMAT",
                has_result=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )        
        try:
            user = User.objects.get(verification_token=token)
            # Check if the token is expired
            if user.token_expiration < timezone.now():
                return custom_response(
                    status=False,
                    message="Token has expired.",
                    error_code="TOKEN_EXPIRED",
                    has_result=False,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # Verify the user
            user.is_verified = True
            user.verification_token = None  # Clear the token after verification
            user.token_expiration = None
            user.save()

            return custom_response(
                status=True,
                message="Email verified successfully.",
                has_result=False,
                status_code=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return custom_response(
                status=False,
                message="Invalid token.",
                error_code="INVALID_TOKEN",
                has_result=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )