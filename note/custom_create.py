from rest_framework.response import Response
from rest_framework import status
from .push_websocket import created_category_error_note_send_notification, created_error_note_send_notification
from rate_limiter.limiter import rate_limiter

MAX_TRIES_CREATE_VIEWS = 5
TIME_IN_SECONDS = 300

class CustomCategoryCreateMixins:
    @rate_limiter(max_requests=int(MAX_TRIES_CREATE_VIEWS), time_window=int(TIME_IN_SECONDS))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            self.get_serializer_error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_serializer_error(self, errors):
        created_category_error_note_send_notification(
            error=errors.get('title')[0].split('string=')[0],
            user_id=self.request.user.id
        )

class CustomNoteCreateMixins:
    @rate_limiter(max_requests=int(MAX_TRIES_CREATE_VIEWS), time_window=int(TIME_IN_SECONDS))
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