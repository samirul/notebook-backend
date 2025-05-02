"""
   Serializer for views.py in accounts 
"""

from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer as DefaultSerializer
from accounts.models import User
from .bloom_filter import bloom_filter


class GetUserSerializer(serializers.ModelSerializer):
    """Serializer for GetUser in views.py

    Args:
        serializers (ModelSerializer): DRF model serializer class for serialization.
    """
    class Meta:
        model = User
        fields = ["id", "username", "email", "profilePic"]



class RegisterSerializer(DefaultSerializer):
    def validate_username(self, username):
        if username in bloom_filter:
            raise serializers.ValidationError("This username already taken.")
        return username