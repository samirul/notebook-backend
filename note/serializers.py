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
    
class NoteItemViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'category', 'note_text', 'created_at', 'updated_at']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = CategoryListViewsSerializer(instance.category).data
        created_at = instance.created_at
        updated_at = instance.updated_at
        rep['created_at'] = created_at.strftime('%Y-%m-%d %I:%M %p')
        rep['updated_at'] = updated_at.strftime('%Y-%m-%d %I:%M %p')
        return {"note": rep}

class CategorySerializerMenu(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = CategoryNotes
        fields = ['id', 'title', 'subcategories']

    def get_subcategories(self, obj):
        notes = obj.notes_category.only('id', 'title')
        return NoteSerializerMenu(notes, many=True).data
    
class CategorySearchViewSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()

class NoteSearchViewSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()


class DownloadFileSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    html = serializers.CharField(required=True)
    selected = serializers.CharField(required=True)

class PDFFileDownloadSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    html = serializers.CharField(required=True)
    selected = serializers.CharField(required=True)

class TXTFileDownloadSerializer(DownloadFileSerializer):
    pass