from django.urls import path
from .views import NewCategoryView

urlpatterns = [
    path('new-notes/', NewCategoryView.as_view(), name='new-notes'),
]