from rest_framework import generics, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (NewCategorySerializer, CategoryListViewsSerializer, NewNoteSerializer,
                        CategorySerializerMenu, CategorySearchViewSerializer)
from .push_websocket import created_category_note_send_notification, created_note_send_notification
from .models import CategoryNotes
from .custom_create import CustomCategoryCreateMixins, CustomNoteCreateMixins
from .documents import CategoryNotesDocument, NotesDocument


class NewCategoryCreateView(CustomCategoryCreateMixins, generics.CreateAPIView):
    serializer_class = NewCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        created_category_note_send_notification(
        instance=instance, user_id=self.request.user.id
        )
        

class CategoryListView(generics.ListAPIView):
    queryset = CategoryNotes.objects.all()
    serializer_class = CategoryListViewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query =  super().get_queryset()
        return query.filter(user=self.request.user)
    
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
    
    def list(self, request, *args, **kwargs):
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "title": "Notes",
                "icon": "FaBook",
                "submenu": serializer.data
            })
    
class CategorySearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = str(request.user.id)
        query = request.query_params.get("q", "")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 5))
        start = (page - 1) * page_size
        results = CategoryNotesDocument.search().query(
            "bool",
            must=[
                {
                    "match": {
                        "title": {
                            "query": query,
                            "fuzziness": "AUTO"
                        }
                    }
                }
            ],
            filter=[
                {
                    "term": {
                        "user": user_id
                    }
                }
            ]
        ).extra(from_=start, size=page_size)
        total_page = results.count()
        results = [{"id": result.meta.id,"title": result.title} for result in results]
        serializer = CategorySearchViewSerializer(results, many=True)
        return Response({"count": total_page,
                        "page": page,
                        "page_size": page_size,
                        "search_result": serializer.data})
