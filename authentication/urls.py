from django.urls import path
from .views import CustomTokenRefreshView, LogoutView, SignupView, LoginView, VerifyEmailView, ChangePasswordView, EditProfileDetailsView, GetProfileDetailsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('edit-profile-details/', EditProfileDetailsView.as_view(), name='edit-profile-details'),
    path('get-profile-details/', GetProfileDetailsView.as_view(), name='get-profile-details'),
]
