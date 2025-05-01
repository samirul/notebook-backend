"""
   Serializer for views.py in accounts 
"""

from rest_framework import serializers
from accounts.models import User


class GetUserSerializer(serializers.ModelSerializer):
    """Serializer for GetUser in views.py

    Args:
        serializers (ModelSerializer): DRF model serializer class for serialization.
    """
    class Meta:
        model = User
        fields = ["id", "username", "email", "profilePic"]