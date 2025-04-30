"""
    JWT Authentication Middleware for Django Channels
    This middleware extracts the JWT token from the query string and authenticates the user.
    It uses the JWT token to retrieve the user ID and set the user in the scope.
"""
from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections

from jwt import (InvalidTokenError, InvalidSignatureError,
                DecodeError, ExpiredSignatureError)
from jwt import decode as jwt_decode


User = get_user_model()

class JWTAuthMiddleware:
    """
        Authenticates users based on JWT tokens passed in the query string.

        Extracts the JWT token, decodes it, and retrieves the corresponding user,
        setting it in the scope for downstream consumers.
    """
    def __init__(self, inner):
        """
            Initializes the JWTAuthMiddleware instance.

            Args:
                inner: The next middleware in the stack.
        """
        self.inner = inner

    async def __call__(self, scope, receive, send):
        """
            Processes the incoming request by authenticating the user via JWT.

            Args:
                scope: The ASGI scope.
                receive: The ASGI receive function.
                send: The ASGI send function.

            Returns:
                The result of calling the next middleware in the stack.
        """
        # Close old database connections
        close_old_connections()
        try:
            # Get the token from the query string
            token = parse_qs(scope["query_string"].decode("utf8")).get("token", None)[0]
            if token is not None:
                # Decode the JWT token
                data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                # Check if the token is valid and extract user ID
                scope['user'] = await self.get_user(data['user_id'])
        except (TypeError, InvalidTokenError, InvalidSignatureError, ExpiredSignatureError, DecodeError):
            scope['user'] = AnonymousUser()
        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        """
            Retrieves the user from the database based on their ID.

            Args:
                user_id: The ID of the user to retrieve.

            Returns:
                The user object if found, otherwise an AnonymousUser instance.
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
        
def jwt_auth_middleware_stack(inner):
    """
        Wraps the inner application with JWT authentication middleware.
    """
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))
