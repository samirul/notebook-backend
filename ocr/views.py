import os
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import OCRFIleUpload
from .serializers import FIleUploadPDFViewsSerializer

class FIleUploadPDFViews(viewsets.ModelViewSet):
    serializer_class = FIleUploadPDFViewsSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['get', 'post', 'delete']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        file_path = instance.file_upload.path
        if os.path.exists(file_path):
            os.remove(file_path)
        instance.delete()

    def get_queryset(self):
        return OCRFIleUpload.objects.filter(user=self.request.user)



