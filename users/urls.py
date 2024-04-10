from django.urls import path
from .views import RegisterView, LogoutView, ResetEmail, OTPVerification
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", RegisterView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("resetEmail/", ResetEmail.as_view(), name="resetEmail"),
    path("resetPassword/", OTPVerification.as_view(), name="resetpassword"),
]
