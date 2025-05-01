"""
    accounts Views for writing code logic for login user using google social login.
"""

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from accounts.serializers import GetUserSerializer


class GoogleLoginViews(SocialLoginView):
    """Added Google Login Views for login with google with dj_rest_auth and all auth.

    Args:
        SocialLoginView (Class): For supporting OAuth2 login, here GoogleOAuth2Adapter is
        for login with google. Will get a code from the frontend after sign-in using google.
        After that will have access token and refresh token.
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8080"
    client_class = OAuth2Client

class GetUser(APIView):
    """For fetching user or user information after login user.

        Args:
            APIView (Class): Django Rest Framework(DRF) API View.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """Will send GET request from frontend reactjs

        Args:
            request (request): Django request argument.

        Returns:
            Response: Return serializer data and status (200 OK)
            if serializer is valid.
        """
        serializer = GetUserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    