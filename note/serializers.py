from rest_framework import serializers
from .models import CategoryNotes


class NewCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryNotes
        fields = ['id', 'category_title']


class CategoryListViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryNotes
        fields = ['id', 'category_title']