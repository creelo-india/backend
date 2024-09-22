from django.urls import path
# from .accounts.views import views
from accounts.views import CreateUserApi, VerifyOTP, LoginAPIView,RequestPasswordResetEmail,Reset_Password_VerifyOTP,EmailVerification
from rest_framework_simplejwt.views import TokenObtainPairView


# VerifyOTP Reset_Password_VerifyOTP
urlpatterns = [
    path('verify-email/', EmailVerification.as_view(), name='verify-email'),
    path('user-register/', CreateUserApi.as_view(), name='user-register'),
    path('otp-verify/', VerifyOTP.as_view(), name='otp-verify'),
    path('user-sign/', LoginAPIView.as_view(), name='user-sign'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user-forget-password/',RequestPasswordResetEmail.as_view(),name='user-forget-password'),
    path('forget-password/',Reset_Password_VerifyOTP.as_view(),name='forget-password'),



]
