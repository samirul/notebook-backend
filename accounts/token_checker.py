""" 
    Token Checker Module
    This module provides a function to authenticate a user based on a JWT token passed in the headers.
"""

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from asgiref.sync import sync_to_async
from jwt import decode as jwt_decode
from jwt import (InvalidTokenError, InvalidSignatureError,
                DecodeError, ExpiredSignatureError)

@sync_to_async
def check_token(headers):
    """Authenticates a user based on a JWT token passed in the headers.

    This function retrieves the 'access_token' from the cookies in the provided headers,
    decodes the JWT, and retrieves the corresponding user from the database.
    If the token is invalid or expired, an AnonymousUser instance is returned.

    Args:
        headers: A list of headers from the request.

    Returns:
        The authenticated user object if the token is valid, otherwise an AnonymousUser instance.
    """
    try:
        token = []
        close_old_connections()
        user = get_user_model()
        for header in headers:
            if header[0].lower() == b'cookie':
                cookie_string = header[1].decode()
                cookies = dict(pair.strip().split('=') for pair in cookie_string.split(';') if '=' in pair)
                token.append(cookies.get("access_token"))
        data = jwt_decode(token[0], settings.SIMPLE_JWT.get('SIGNING_KEY'), algorithms=["HS256"])
        return user.objects.only('email').get(id=data['user_id'])
    except (TypeError, ValueError, InvalidTokenError, InvalidSignatureError, ExpiredSignatureError, DecodeError):
            user = AnonymousUser()
            return user