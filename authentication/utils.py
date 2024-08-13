from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

def custom_response(status=True, message='', error_code='', result=None, has_result=True, status_code=200):
    return Response({
        'status': status,
        'message': message,
        'errorCode': error_code,
        'result': result,
        'hasResult': has_result
    }, status=status_code)


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

