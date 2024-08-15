from authentication.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError


class UserService:
    @staticmethod
    def create_user(validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                date_of_birth=validated_data['date_of_birth'],
                gender=validated_data['gender'],
                phone_number=validated_data['phone_number'],
                address=validated_data['address']
            )
            user.save()
            return user
        except IntegrityError as e:
            # Handle cases where the username or email might already be taken
            raise ValidationError(f"User creation failed: {str(e)}")
        except Exception as e:
            # Handle other unexpected errors
            raise ValidationError(f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def update_user(user: User, validated_data):
        try:
            user.first_name = validated_data.get('first_name', user.first_name)
            user.last_name = validated_data.get('last_name', user.last_name)
            user.date_of_birth = validated_data.get('date_of_birth', user.date_of_birth)
            user.gender = validated_data.get('gender', user.gender)
            user.phone_number = validated_data.get('phone_number', user.phone_number)
            user.address = validated_data.get('address', user.address)
            
            user.save()
            return user
        except IntegrityError as e:
            # Handle potential database integrity errors
            raise ValidationError(f"User update failed: {str(e)}")
        except Exception as e:
            # Handle other unexpected errors
            raise ValidationError(f"An unexpected error occurred: {str(e)}")
