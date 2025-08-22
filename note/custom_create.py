import os
import configparser
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from rate_limiter.limiter import rate_limiter
from .push_websocket import created_category_error_note_send_notification, created_error_note_send_notification


file_dir = os.path.dirname(__file__)
config = configparser.ConfigParser()

# Make a full path to the config file
config_file_path_ini = os.path.join(file_dir, '../rate_limiter/config/', 'rate_limit.ini')
# Read ini file
config.read(config_file_path_ini)
# Fetch ini configs
max_tries_create_views = config.get('configuration', 'MAX_TRIES_CREATE_VIEWS')
max_time_in_seconds = config.get('configuration', 'MAX_TIME_IN_SECONDS')


class CustomCategoryCreateMixins:
    @rate_limiter(max_requests=int(max_tries_create_views), time_window=int(max_time_in_seconds))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            self.get_serializer_error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        key = {"key_cache_categories": f"user_category_user_id_{request.user.id}_cache"}
        cache.delete(key=key.get("key_cache_categories"))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_serializer_error(self, errors):
        created_category_error_note_send_notification(
            error=errors.get('title')[0].split('string=')[0],
            user_id=self.request.user.id
        )

class CustomNoteCreateMixins:
    @rate_limiter(max_requests=int(max_tries_create_views), time_window=int(max_time_in_seconds))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            self.get_serializer_error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_serializer_error(self, errors):
        if errors.get('note_text'):
            created_error_note_send_notification(
                error=errors.get('note_text')[0].split('string=')[0],
                user_id=self.request.user.id
            )
        elif errors.get('title'):
            created_error_note_send_notification(
                error=errors.get('title')[0].split('string=')[0],
                user_id=self.request.user.id
            )
        elif errors.get('category'):
            created_error_note_send_notification(
                error=errors.get('category')[0].split('string=')[0],
                user_id=self.request.user.id
            )