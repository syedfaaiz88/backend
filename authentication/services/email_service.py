from django.core.mail import send_mail
from django.conf import settings
from authentication.models import User
import uuid
from rest_framework.exceptions import ValidationError
from django.utils import timezone

class EmailService:
    @staticmethod
    def send_verification_email(user):
        token = user.generate_verification_token()
        verification_link = f"{settings.FRONTEND_URL}/verify-email/{token}"
        send_mail(
            'Verify your email',
            f"Please click the following link to verify your email: {
                verification_link}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    @staticmethod
    def verify_email_token(token):
        # Validate the token format
        try:
            uuid.UUID(token)
        except ValueError:
            raise ValidationError("Invalid token format.","INVALID_TOKEN_FORMAT")

        try:
            user = User.objects.get(verification_token=token)

            if user.is_verified:
                raise ValidationError("User is already verified.", "ALREADY_VERIFIED")

            if user.token_expiration < timezone.now():
                raise ValidationError("Token has expired.", "TOKEN_EXPIRED")

            # Verify the user
            user.is_verified = True
            user.verification_token = None
            user.token_expiration = None
            user.save()

            return user
        except User.DoesNotExist:
            raise ValidationError("Invalid token.", "INVALID_TOKEN")
        
    # @staticmethod
    # def send_password_reset_email(user: User, reset_token: str):
    #     reset_link = f"{settings.FRONTEND_URL}/reset-password/{reset_token}/"
    #     subject = 'Password Reset Request'
    #     message = render_to_string('email/password_reset_email.html', {
    #         'user': user,
    #         'reset_link': reset_link,
    #     })
        
    #     send_mail(
    #         subject,
    #         message,
    #         settings.DEFAULT_FROM_EMAIL,
    #         [user.email],
    #         fail_silently=False,
    #     )
