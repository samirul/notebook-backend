from rest_framework import serializers
from .models import CategoryNotes, Notes


class NewCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryNotes
        fields = ['id', 'title']


class CategoryListViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryNotes
        fields = ['id', 'title']

class NewNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'category', 'note_text']

class NoteSerializerMenu(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()

    class Meta:
        model = Notes
        fields = ['id', 'title', 'path']

    def get_path(self, obj):
        return f"/note/{obj.id}"

class CategorySerializerMenu(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = CategoryNotes
        fields = ['id', 'title', 'subcategories']

    def get_subcategories(self, obj):
        notes = obj.notes_category.only('id', 'title')
        return NoteSerializerMenu(notes, many=True).data