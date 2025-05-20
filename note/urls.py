from django.urls import path
from .views import NewCategoryCreateView, CategoryListView, NewNoteCreateView

urlpatterns = [
    path('new-category/', NewCategoryCreateView.as_view(), name='new-category'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('new-note/', NewNoteCreateView.as_view(), name='new-note'),
]