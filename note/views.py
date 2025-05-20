from rest_framework import generics, permissions
from .serializers import NewCategorySerializer, CategoryListViewsSerializer
from .push_websocket import created_category_note_send_notification
from .models import CategoryNotes


class NewCategoryCreateView(generics.CreateAPIView):
    serializer_class = NewCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        created_category_note_send_notification(
        instance=instance, user_id=self.request.user.id
        )

class CategoryListView(generics.ListAPIView):
    queryset = CategoryNotes.objects.all()
    serializer_class = CategoryListViewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query =  super().get_queryset()
        return query.filter(user=self.request.user)