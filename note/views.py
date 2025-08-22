import os
import configparser
from django.core.cache import cache
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (NewCategorySerializer, CategoryListViewsSerializer, NewNoteSerializer,
                        CategorySerializerMenu, NoteItemViewSerializer)
from .push_websocket import (created_category_note_send_notification, created_note_send_notification,
                             deleted_category_note_send_notification, deleted_note_send_notification)
from .models import CategoryNotes, Notes
from .custom_create import CustomCategoryCreateMixins, CustomNoteCreateMixins
from .elastic.elastic_category import elastic_search_category, elastic_search_note
from .task.task import delete_category_instance_from_elastic_search, delete_note_instance_from_elastic_search
from rate_limiter.limiter import rate_limiter


file_dir = os.path.dirname(__file__)
config = configparser.ConfigParser()

# Make a full path to the config file
config_file_path_ini = os.path.join(file_dir, '../rate_limiter/config/', 'rate_limit.ini')
# Read ini file
config.read(config_file_path_ini)
# Fetch ini configs
max_tries_get_views = config.get('configuration', 'MAX_TRIES_GET_VIEWS')
max_tries_update_views = config.get('configuration', 'MAX_TRIES_UPDATE_VIEWS')
max_tries_delete_views = config.get('configuration', 'MAX_TRIES_DELETE_VIEWS')
max_tries_search_views = config.get('configuration', 'MAX_TRIES_SEARCH_VIEWS')
max_time_in_seconds = config.get('configuration', 'MAX_TIME_IN_SECONDS')


class NewCategoryCreateView(CustomCategoryCreateMixins, generics.CreateAPIView):
    serializer_class = NewCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        created_category_note_send_notification(
        instance=instance, user_id=self.request.user.id
        )
        

class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryListViewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CategoryNotes.objects.filter(user=self.request.user)
    
    @rate_limiter(max_requests=int(max_tries_get_views), time_window=int(max_time_in_seconds))
    def list(self, request, *args, **kwargs):
        key = {"key_cache": f"user_category_user_id_{request.user.id}_cache"}
        cache_data = cache.get(key=key.get("key_cache"))
        if cache_data is not None:
            return Response(cache_data)
        instance = super().list(request, *args, **kwargs)
        cache.set(key.get("key_cache"), instance.data, timeout=300)
        return Response(instance.data)


class CategoryDestroyView(generics.DestroyAPIView):
    serializer_class = CategoryListViewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CategoryNotes.objects.filter(user=self.request.user)
    
    @rate_limiter(max_requests=int(max_tries_delete_views), time_window=int(max_time_in_seconds))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        category_title = instance.title
        delete_category_instance_from_elastic_search.delay(instance_id=instance.id)
        self.perform_destroy(instance=instance)
        deleted_category_note_send_notification(instance=category_title,
                                                user_id=self.request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

 
class NewNoteCreateView(CustomNoteCreateMixins, generics.CreateAPIView):
    serializer_class = NewNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
       instance = serializer.save(user=self.request.user)
       created_note_send_notification(
       instance=instance, user_id=self.request.user.id
       )


class NotesListView(generics.ListAPIView):
    queryset = CategoryNotes.objects.prefetch_related('notes_category')
    serializer_class = CategorySerializerMenu
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query =  super().get_queryset()
        return query.filter(user=self.request.user)
    
    @rate_limiter(max_requests=int(max_tries_get_views), time_window=int(max_time_in_seconds))
    def list(self, request, *args, **kwargs):
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "title": "Notes",
                "icon": "FaBook",
                "submenu": serializer.data
            })


class NoteItemView(generics.RetrieveAPIView):
    serializer_class = NoteItemViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notes.objects.filter(user=self.request.user)
    
    @rate_limiter(max_requests=int(max_tries_get_views), time_window=int(max_time_in_seconds))
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        key = {"key_cache": f"user_notes_id_{pk}_user_id_{request.user.id}_cache"}
        cache_data = cache.get(key=key.get("key_cache"))
        if cache_data is not None:
            return Response(cache_data)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        cache.set(key.get("key_cache"), data, timeout=300)
        return Response(data)


class NoteUpdateView(generics.UpdateAPIView):
    serializer_class = NoteItemViewSerializer
    http_method_names = ['patch']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notes.objects.filter(user=self.request.user)
    
    @rate_limiter(max_requests=int(max_tries_update_views), time_window=int(max_time_in_seconds))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.save()
        key = {"key_cache": f"user_notes_id_{instance.id}_user_id_{self.request.user.id}_cache"}
        cache.delete(key=key.get("key_cache"))
        

class NoteDestroyView(generics.DestroyAPIView):
    serializer_class = NewNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notes.objects.filter(user=self.request.user)
    
    @rate_limiter(max_requests=int(max_tries_delete_views), time_window=int(max_time_in_seconds))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = kwargs.get('pk')
        key = {"key_cache": f"user_notes_id_{pk}_user_id_{request.user.id}_cache"}
        category_title = instance.title
        cache.delete(key.get("key_cache"))
        delete_note_instance_from_elastic_search.delay(instance_id=instance.id)
        self.perform_destroy(instance=instance)
        deleted_note_send_notification(instance=category_title,
                                                user_id=self.request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class CategorySearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    @rate_limiter(max_requests=int(max_tries_search_views), time_window=int(max_time_in_seconds))
    def get(self, request):
        total_page, page, page_size, serializer = elastic_search_category(request=request)
        return Response({"count": total_page,
                        "page": page,
                        "page_size": page_size,
                        "search_result": serializer.data})
    
class NoteSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    @rate_limiter(max_requests=int(max_tries_search_views), time_window=int(max_time_in_seconds))
    def get(self, request):
        total_page, page, page_size, serializer = elastic_search_note(request=request)
        return Response({"count": total_page,
                        "page": page,
                        "page_size": page_size,
                        "search_result": serializer.data})
