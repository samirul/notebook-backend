from rest_framework.routers import DefaultRouter
from .views import FIleUploadPDFViews

router = DefaultRouter()
router.register(r'upload', FIleUploadPDFViews, basename='upload-pdf-file')
urlpatterns = router.urls
