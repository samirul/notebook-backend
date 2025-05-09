"""
   Serializer for views.py in accounts 
"""
import os
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer as DefaultSerializer
from accounts.models import User
from .bloom_filter import connect_redis
# from .bloom_filter import bloom_filter


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
        redis_client = connect_redis()
        key = os.environ.get('REDIS_BLOOM_KEY')
        bloom_filter_username_check = redis_client.execute_command('BF.EXISTS', key, username)
        if bloom_filter_username_check == 1:
            raise serializers.ValidationError("This username already taken.")
        return username