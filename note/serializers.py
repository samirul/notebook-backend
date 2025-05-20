from rest_framework import serializers
from .models import CategoryNotes, Notes


class NewCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryNotes
        fields = ['id', 'category_title']


class CategoryListViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryNotes
        fields = ['id', 'category_title']

class NewNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'note_title', 'category', 'note_text']