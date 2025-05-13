"""
    Added models from accounts app inside admin
    so can register inside control panel(can view data from
    django admin panel).
"""

from django.contrib import admin
from django.apps import apps
from .models import CategoryNotes, Notes

@admin.register(CategoryNotes)
class CategoryNotesModelAdmin(admin.ModelAdmin):
    """Register CategoryNotes model.

    Args:
        admin (class ModelAdmin): For registering in the admin panel.
    """
    list_display = [
      'id', 'category_title'
    ]

@admin.register(Notes)
class NotesModelAdmin(admin.ModelAdmin):
    """Register Notes model.

    Args:
        admin (class ModelAdmin): For registering in the admin panel.
    """
    list_display = [
      'id', 'note_title', 'note_text'
    ]


apps.get_app_config('note').verbose_name = "Notes"