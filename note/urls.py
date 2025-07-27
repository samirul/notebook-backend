from django.urls import path
from .views import (NewCategoryCreateView, CategoryListView, NewNoteCreateView,
                    NotesListView, NoteItemView, CategorySearchView, CategoryDestroyView, NoteSearchView,
                    NoteDestroyView)

urlpatterns = [
    path('new-category/', NewCategoryCreateView.as_view(), name='new-category'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('new-note/', NewNoteCreateView.as_view(), name='new-note'),
    path('notes/', NotesListView.as_view(), name='notes'),
    path('notes/<str:pk>/', NoteItemView.as_view(), name='notes'),
    path('category/search/', CategorySearchView.as_view(), name='category-search'),
    path('category/delete/<str:pk>/', CategoryDestroyView.as_view(), name='category-delete'),
    path('note/search/', NoteSearchView.as_view(), name='note-search'),
    path('note/delete/<str:pk>/', NoteDestroyView.as_view(), name='note-delete'),
]