from rest_framework import generics, permissions
from .serializers import NewCategorySerializer


class NewCategoryView(generics.CreateAPIView):
    serializer_class = NewCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
