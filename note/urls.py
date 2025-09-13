from django.urls import path
from .views import (NewCategoryCreateView, CategoryListView, NewNoteCreateView,
                    NotesListView, NoteItemView, CategorySearchView, CategoryDestroyView, NoteSearchView,
                    NoteUpdateView, NoteDestroyView, PDFDownloader, StatusView, GetPDFFileView, DownloadTXT,
                    GetTextFileView)

urlpatterns = [
    # Category
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('new-category/', NewCategoryCreateView.as_view(), name='new-category'),
    path('category/search/', CategorySearchView.as_view(), name='category-search'),
    path('category/delete/<str:pk>/', CategoryDestroyView.as_view(), name='category-delete'),
    # Note
    path('notes/', NotesListView.as_view(), name='notes'),
    path('new-note/', NewNoteCreateView.as_view(), name='new-note'),
    path('notes/<str:pk>/', NoteItemView.as_view(), name='notes'),
    path('note/search/', NoteSearchView.as_view(), name='note-search'),
    path('note/<str:pk>/update/', NoteUpdateView.as_view(), name='note-update'),
    path('note/delete/<str:pk>/', NoteDestroyView.as_view(), name='note-delete'),
    # celery status
    path('status/<str:task_id>/', StatusView.as_view(), name='status'),
    # PDF Download
    path('note/download/pdf/', PDFDownloader.as_view(), name='pdf-download'),
    path('media/pdf/<str:filename>/', GetPDFFileView.as_view(), name='download-pdf'),
    # TXT Download
    path('note/download/text/', DownloadTXT.as_view(), name='txt-download'),
    path('media/text/<str:filename>/', GetTextFileView.as_view(), name='download-text'),
]