from django.urls import path

from apps.users.views import RefreshTokenView, OTPLoginView



urlpatterns = [
    path('register/', OTPLoginView.as_view(), name='login'),
    path('refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),
]
