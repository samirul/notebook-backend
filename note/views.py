import os
import configparser
import contextlib
from django.core.cache import cache
from django.http import FileResponse
from django.conf import settings
from celery.result import AsyncResult
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rate_limiter.limiter import rate_limiter
from .serializers import (NewCategorySerializer, CategoryListViewsSerializer, NewNoteSerializer,
                        CategorySerializerMenu, NoteItemViewSerializer, PDFFileDownloadSerializer)
from .push_websocket import (created_category_note_send_notification, created_note_send_notification,
                             deleted_category_note_send_notification, deleted_note_send_notification,
                             update_note_send_notification)
from .models import CategoryNotes, Notes
from .custom_create import CustomCategoryCreateMixins, CustomNoteCreateMixins, clear_caches
from .elastic.elastic_category import elastic_search_category, elastic_search_note
from .task.task import download_pdf


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
        cache_data = cache.get(key=str(key.get("key_cache")))
        if cache_data is not None:
            return Response(cache_data)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        cache.set(key.get("key_cache"), serializer.data, timeout=300)
        return Response(serializer.data)


class CategoryDestroyView(generics.DestroyAPIView):
    serializer_class = CategoryListViewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CategoryNotes.objects.filter(user=self.request.user)
    
    @rate_limiter(max_requests=int(max_tries_delete_views), time_window=int(max_time_in_seconds))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        category_title = instance.title
        self.perform_destroy(instance=instance)
        clear_caches(user=request.user)
        deleted_category_note_send_notification(instance=category_title,
                                            user_id=self.request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

 
class NewNoteCreateView(CustomNoteCreateMixins, generics.CreateAPIView):
    serializer_class = NewNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
       instance = serializer.save(user=self.request.user)
       created_note_send_notification(
       instance=instance, user_id=self.request.user.id # type: ignore
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
        key = {"key_cache": f"user_notes_user_id_{request.user.id}_cache"}
        cache_data = cache.get(key=str(key.get("key_cache")))
        if cache_data is not None:
            return Response(cache_data)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "title": "Notes",
            "icon": "FaBook",
            "submenu": serializer.data 
        }
        cache.set(key.get("key_cache"), data, timeout=300)
        return Response(data)


class NoteItemView(generics.RetrieveAPIView):
    serializer_class = NoteItemViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notes.objects.filter(user=self.request.user)
    
    @rate_limiter(max_requests=int(max_tries_get_views), time_window=int(max_time_in_seconds))
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        key = {"key_cache": f"user_notes_id_{pk}_user_id_{request.user.id}_cache"}
        cache_data = cache.get(key=str(key.get("key_cache")))
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
        clear_caches(user=self.request.user, pk=instance.id)
        update_note_send_notification(instance=instance,
                                            user_id=self.request.user.id)
        

class NoteDestroyView(generics.DestroyAPIView):
    serializer_class = NewNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notes.objects.filter(user=self.request.user)
    
    @rate_limiter(max_requests=int(max_tries_delete_views), time_window=int(max_time_in_seconds))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        clear_caches(user=request.user, pk=kwargs.get('pk'))
        self.perform_destroy(instance=instance)
        deleted_note_send_notification(instance=instance.title,
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
    
def download_pdf_delay_task(request, serializer):
    selected = serializer.validated_data.get("selected", "")
    if selected != 'pdf-file':
        return Response({"error": "Pdf only required"}, status=status.HTTP_400_BAD_REQUEST)
    payload = {
        "auth_user_id": request.user.id,
        "user_access_token": request.COOKIES.get('access_token'),
        "name": serializer.validated_data.get("name", ""),
        "html_content": serializer.validated_data.get("html", "")
    }
    return download_pdf.delay(payload) # type: ignore



def download_pdf_file(request):
    data_item_id = {}
    serializer = PDFFileDownloadSerializer(data=request.data.get('data'))
    if serializer.is_valid():
        pdf_result = download_pdf_delay_task(request, serializer)
        data_item_id['pdf_download_task_id'] = pdf_result.id # type: ignore
    return data_item_id


class PDFDownloader(APIView):
    http_method_names = ['post']
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        status_id = download_pdf_file(request=request)
        return Response(status_id, status=status.HTTP_202_ACCEPTED)

def get_status(task_id):
    task = AsyncResult(task_id)
    response_data = {
        "FAILURE": {'status': 'FAILURE', 'error': str(task.result)},
        "PENDING": {'status': 'PENDING'},
        "SUCCESS": {'status': 'SUCCESS', 'pdf_url': task.result}                                            
    }
    return response_data.get(task.state, {'status': task.state})


class PdfStatusView(APIView):
    http_method_names = ['get']
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, task_id):
        response_data = get_status(task_id)
        return Response(response_data)
    

class GetPDFFileView(APIView):
    http_method_names = ['get']
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, filename):
        with contextlib.suppress(FileNotFoundError):
            file_path = os.path.join(f"{settings.MEDIA_ROOT}pdf/", filename)
            if os.path.exists(file_path):
                response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
        
        

