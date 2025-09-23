from rest_framework import serializers
from .models import OCRFIleUpload

class FIleUploadPDFViewsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = OCRFIleUpload
        fields = ['id', 'title', 'file_upload', 'created_at']