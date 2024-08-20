from rest_framework import generics
from rest_framework.permissions import AllowAny

from authentication.services.email_service import EmailService
from .models import User
from .serializers import UserSerializer, LoginSerializer
from .services.auth_service import AuthService
from .utils.custom_response import custom_response
from rest_framework import status
from rest_framework.exceptions import ValidationError

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        try:
            password = self.request.data.get('password')
            user = serializer.save()
            user.set_password(password)
            user.save()

            # Send verification email
            EmailService.send_verification_email(user)

            return custom_response(
                status=True,
                message=f"Verification email sent to {user.email}. Please verify your account.",
                result=UserSerializer(user).data,
                has_result=True,
                status_code=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            # Handle known validation errors
            return custom_response(
                status=False,
                message=str(e.detail[0]),
                error_code=str(e.detail[0].code),
                has_result=False,
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            # Handle unexpected errors
            return custom_response(
                status=False,
                message=f"An unexpected error occurred: {str(e)}",
                error_code="UNKNOWN_ERROR",
                has_result=False,
                status_code=status.HTTP_200_OK
            )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return custom_response(
                status=False,
                message="Validation errors.",
                error_code="VALIDATION_ERROR",
                errors=serializer.errors,
                has_result=False,
                status_code=status.HTTP_200_OK
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
                message="Validation errors.",
                error_code="VALIDATION_ERROR",
                errors=serializer.errors,
                has_result=False,
                status_code=status.HTTP_200_OK
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
                status_code=status.HTTP_200_OK
            )

        if not user.is_verified:
            EmailService.send_verification_email(user)
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
            user = EmailService.verify_email_token(token)
            return custom_response(
                status=True,
                message="Email verified successfully.",
                has_result=False,
                status_code=status.HTTP_200_OK
            )
        except ValidationError as e:
            return custom_response(
                status=False,
                message=str(e.detail[0]),
                error_code=str(e.detail[0].code),
                has_result=False,
                status_code=status.HTTP_200_OK
            )