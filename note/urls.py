from django.urls import path
from .views import NewCategoryCreateView, CategoryListView

urlpatterns = [
    path('new-notes/', NewCategoryCreateView.as_view(), name='new-notes'),
    path('categories/', CategoryListView.as_view(), name='categories'),
]