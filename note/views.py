from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from .serializers import (NewCategorySerializer, CategoryListViewsSerializer, NewNoteSerializer,
                        CategorySerializerMenu)
from .push_websocket import created_category_note_send_notification
from .models import CategoryNotes
from .custom_create import CustomCreateMixins


class NewCategoryCreateView(CustomCreateMixins, generics.CreateAPIView):
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
    
class NewNoteCreateView(generics.CreateAPIView):
    serializer_class = NewNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
       serializer.save(user=self.request.user)

class NotesListView(generics.ListAPIView):
    queryset = CategoryNotes.objects.prefetch_related('notes_category')
    serializer_class = CategorySerializerMenu
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query =  super().get_queryset()
        return query.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "title": "Notes",
                "icon": "FaBook",
                "submenu": serializer.data
            })
