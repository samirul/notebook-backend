from django.contrib import admin
from .models import OCRFIleUpload, OCRModel

@admin.register(OCRFIleUpload)
class OCRUploadAdminModel(admin.ModelAdmin):
    """Register OCRFIleUpload model.

    Args:
        admin (class ModelAdmin): For registering in the admin panel.
    """
    list_display = [
      'title', 'file_upload'
    ]

@admin.register(OCRModel)
class OCRAdminModel(admin.ModelAdmin):
    """Register OCRModel model.

    Args:
        admin (class ModelAdmin): For registering in the admin panel.
    """
    list_display = [
      'name', 'content'
    ]