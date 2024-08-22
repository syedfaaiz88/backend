from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
import uuid
from django.conf import settings

from common.models.base_model import BaseModel
from common.models.models import Gender

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=False, null=False)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, blank=False, null=False)
    bio = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(blank=True, null=True, default=None)
    token_expiration = models.DateTimeField(blank=True, null=True, default=None)

    # Important fields for Django's admin and authentication system
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Additional fields for password reset and account management
    last_login = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def generate_verification_token(self):
        self.verification_token = uuid.uuid4()
        expiration_duration = settings.TOKEN_EXPIRATION_DURATION
        self.token_expiration = timezone.now() + timezone.timedelta(minutes=expiration_duration)
        self.save()
        return self.verification_token
    
    def __str__(self):
        return self.username
