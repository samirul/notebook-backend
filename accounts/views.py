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
from accounts.serializers import GetUserSerializer, CheckLoggedUserStatusSerializer

class CustomGoogleOAuth2Client(OAuth2Client):
    def __init__(
        self,
        request,
        consumer_key,
        consumer_secret,
        access_token_method,
        access_token_url,
        callback_url,
        _scope,  # This is fix for incompatibility between django-allauth==65.2.0 and dj-rest-auth==7.0.1
        scope_delimiter=" ",
        headers=None,
        basic_auth=False,
    ):
        super().__init__(
            request,
            consumer_key,
            consumer_secret,
            access_token_method,
            access_token_url,
            callback_url,
            scope_delimiter,
            headers,
            basic_auth,
        )


class GoogleLoginViews(SocialLoginView):
    """Added Google Login Views for login with google with dj_rest_auth and all auth.

    Args:
        SocialLoginView (Class): For supporting OAuth2 login, here GoogleOAuth2Adapter is
        for login with google. Will get a code from the frontend after sign-in using google.
        After that will have access token and refresh token.
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:5173"
    client_class = CustomGoogleOAuth2Client

class CheckLoggedUserStatus(APIView):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        status_item = {'logged_in': 'yes' if access_token is not None else 'no'}
        serializer = CheckLoggedUserStatusSerializer(status_item)
        return Response({'item': serializer.data}, status=status.HTTP_200_OK)
        

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
    