from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer, LoginSerializer
from .services.auth_service import AuthService
from .utils import custom_response  # Import your custom response function

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        user = serializer.save()
        user.set_password(password)
        user.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return custom_response(
            status=True,
            message="User created successfully.",
            result=serializer.data,
            has_result=True,
            status_code=201
        )

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        auth_response = AuthService.login(email=email, password=password, data=request.data)
        if auth_response:
            return custom_response(
                status=True,
                message="Login successful.",
                result=auth_response,
                has_result=True,
                status_code=200
            )
        return custom_response(
            status=False,
            message="Invalid credentials.",
            error_code="INVALID_CREDENTIALS",
            has_result=False,
            status_code=400
        )
