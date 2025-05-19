from rest_framework import generics, permissions
from .serializers import NewCategorySerializer
from .push_websocket import created_category_note_send_notification





class NewCategoryCreateView(generics.CreateAPIView):
    serializer_class = NewCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        created_category_note_send_notification(
        instance=instance, user_id=self.request.user.id
        )
