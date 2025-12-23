"""
    Added google social login and access token and refresh token login urls.
"""

from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import GoogleLoginViews, GetUser, CheckLoggedUserStatus

urlpatterns = [
    path("social/login/google/", GoogleLoginViews.as_view(), name='google'),
    path('account/', include('allauth.urls')),
    path('user/<str:token>/', GoogleLoginViews.as_view(), name='user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logged/status/', CheckLoggedUserStatus.as_view(), name="logged_status"),
    path('user/', GetUser.as_view(), name='get_user'),
    
]