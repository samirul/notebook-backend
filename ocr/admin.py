from django.contrib import admin
from .models import OCRModel

@admin.register(OCRModel)
class CategoryNotesModelAdmin(admin.ModelAdmin):
    """Register OCRModel model.

    Args:
        admin (class ModelAdmin): For registering in the admin panel.
    """
    list_display = [
      'name', 'content'
    ]