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

class NoteSerializerMenu(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()

    class Meta:
        model = Notes
        fields = ['id', 'note_title', 'path']

    def get_path(self, obj):
        return f"/notes/{obj.id}"

class CategorySerializerMenu(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = CategoryNotes
        fields = ['id', 'category_title', 'subcategories']

    def get_subcategories(self, obj):
        notes = obj.notes_category.only('id', 'note_title')
        return NoteSerializerMenu(notes, many=True).data