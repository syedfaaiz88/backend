from services.auth_service import AuthService
from services.email_service import EmailService
from utils.api_responses import custom_response
from .models import User
from .serializers import ChangePasswordSerializer, UserSerializer, LoginSerializer, EditProfileDetailsSerializer, EditProfilePictureSerializer
from utils.upload_profile_picture import upload_profile_picture
from smtplib import SMTPException

from django.conf import settings

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        try:
            # Retrieve and process the email
            email = self.request.data.get('email', '').strip().lower()
            password = self.request.data.get('password')

            # Pass processed email to the serializer for user creation
            user = serializer.save(email=email)
            user.set_password(password)
            user.save()

            # Attempt to send the verification email
            try:
                EmailService.send_verification_email(user)
            except SMTPException as e:
                return custom_response(
                    status=False,
                    message="User created, but failed to send verification email. Please contact support.",
                    error_code="EMAIL_ERROR",
                    result=UserSerializer(user).data,
                    has_result=True,
                    status_code=status.HTTP_201_CREATED
                )

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
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
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
    authentication_classes = []

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
        email = email.strip().lower()
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
            try:
                EmailService.send_verification_email(user)
            except SMTPException as e:
                return custom_response(
                    status=False,
                    message="User existed, but failed to send verification email. Please contact support.",
                    error_code="EMAIL_ERROR",
                    result=UserSerializer(user).data,
                    has_result=True,
                    status_code=status.HTTP_201_CREATED
                )
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
    authentication_classes = []

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
        
class CustomTokenRefreshView(TokenRefreshView):
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        try:
            # Attempt to refresh the token
            response = super().post(request, *args, **kwargs)
            # If successful, return a custom response
            return custom_response(
                status=True,
                message="Token refreshed successfully.",
                result=response.data,
                has_result=True,
                status_code=status.HTTP_200_OK
            )
        except (InvalidToken, TokenError) as e:
            # Handle token errors with a custom response
            return custom_response(
                status=False,
                message="Token is invalid or expired.",
                error_code="TOKEN_ERROR",
                has_result=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Handle unexpected errors with a custom response
            return custom_response(
                status=False,
                message=f"An unexpected error occurred: {str(e)}",
                error_code="UNKNOWN_ERROR",
                has_result=False,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LogoutView(generics.GenericAPIView):
    authentication_classes = []
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return custom_response(
                status=False,
                message="Refresh token is required.",
                error_code="MISSING_TOKEN",
                has_result=False,
                status_code=status.HTTP_200_OK
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return custom_response(
                    status=True,
                    message="Logout successful.",
                    has_result=False,
                    status_code=status.HTTP_200_OK
                )
            
        except TokenError as e:
            # TokenError is raised for invalid tokens (e.g., wrong token type, expired token)
            return custom_response(
                status=False,
                message="Invalid token.",
                error_code="INVALID_TOKEN",
                errors=str(e),
                has_result=False,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            # Handle unexpected errors
            return custom_response(
                status=False,
                message="An unexpected error occurred during logout.",
                error_code="LOGOUT_ERROR",
                errors=str(e),
                has_result=False,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
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
                
            user = request.user
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            again_new_password = serializer.validated_data.get('again_new_password')

            # Verify old password
            if not user.check_password(old_password):
                return custom_response(
                    status=False,
                    message="Old password is incorrect.",
                    error_code="INVALID_OLD_PASSWORD",
                    has_result=False,
                    status_code=status.HTTP_200_OK
                )

            # Check if new passwords match
            if new_password != again_new_password:
                return custom_response(
                    status=False,
                    message="New passwords do not match.",
                    error_code="PASSWORD_MISMATCH",
                    has_result=False,
                    status_code=status.HTTP_200_OK
                )
            if user.check_password(new_password):
                return custom_response(
                    status=False,
                    message="Your old Password can't be your new password.",
                    error_code="PASSWORD_MATCH_WITH_OLD",
                    has_result=False,
                    status_code=status.HTTP_200_OK
                )
            # Set the new password
            user.set_password(new_password)
            user.save()


            return custom_response(
                status=True,
                message="Password changed successfully.",
                has_result=False,
                status_code=status.HTTP_200_OK
            )      
        except Exception as e:
            return custom_response(
                status=False,
                message=f"An unexpected error occurred: {str(e)}",
                error_code="UNKNOWN_ERROR",
                has_result=False,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class EditProfileDetailsView(generics.GenericAPIView):
    serializer_class = EditProfileDetailsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
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
                
            user = request.user

            # Get validated data if available, otherwise use current user data
            first_name = serializer.validated_data.get('first_name', user.first_name)
            last_name = serializer.validated_data.get('last_name', user.last_name)
            user_name = serializer.validated_data.get('user_name', user.username)
            address = serializer.validated_data.get('address', user.address)
            bio = serializer.validated_data.get('bio', user.bio)
            # Update user fields
            user.first_name = first_name
            user.last_name = last_name
            user.username = user_name
            user.address = address
            user.bio = bio
            user.save()

            # Return success response
            return custom_response(
                status=True,
                message="Profile updated successfully.",
                result=UserSerializer(user).data,
                has_result=True,
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            # Handle unexpected errors
            return custom_response(
                status=False,
                message=f"An unexpected error occurred: {str(e)}",
                error_code="UNKNOWN_ERROR",
                has_result=False,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetProfileDetailsView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Get the authenticated user
            user = request.user

            # Serialize the user data
            serializer = self.get_serializer(user)

            # Return the user profile details in a custom response
            return custom_response(
                status=True,
                message="User profile details retrieved successfully.",
                result=serializer.data,
                has_result=True,
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            # Handle unexpected errors
            return custom_response(
                status=False,
                message=f"An unexpected error occurred: {str(e)}",
                error_code="UNKNOWN_ERROR",
                has_result=False,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class EditProfilePictureView(generics.GenericAPIView):
    serializer_class = EditProfilePictureSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
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
                
            user = request.user
            profile_picture = serializer.validated_data.get('profile_picture')

            # Use the outsourced function to upload the image and get the path
            image_path = upload_profile_picture(user, profile_picture)
            # Update the user's profile_picture field with the new image path
            user.profile_picture = image_path
            user.save()

            # Return success response with updated user profile
            return custom_response(
                status=True,
                message="Profile picture updated successfully.",
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            # Handle unexpected errors
            return custom_response(
                status=False,
                message=f"An unexpected error occurred: {str(e)}",
                error_code="UNKNOWN_ERROR",
                has_result=False,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )                