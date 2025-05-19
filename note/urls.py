from django.urls import path
from .views import NewCategoryCreateView

urlpatterns = [
    path('new-notes/', NewCategoryCreateView.as_view(), name='new-notes'),
]