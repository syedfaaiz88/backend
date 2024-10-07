from django.core.exceptions import ValidationError

def validate_password_strength(password):
    if len(password) < 8 or not any(char.isupper() for char in password) or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in password):
        raise ValidationError(
            'Password must be at least 8 characters long, contain one uppercase letter and one special character.')
