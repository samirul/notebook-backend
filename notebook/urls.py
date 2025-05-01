"""
    Added dj_rest_auth registration, login, password-reset, password-change urls
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/", include('dj_rest_auth.urls')), # login user by username and password
    path("password-reset/confirm/<uidb64>/<token>/", TemplateView.as_view(template_name="account/email/password_reset_confirm.html"), name='password_reset_confirm'),
    path('api/registration/', include('dj_rest_auth.registration.urls')),
    path("accounts/", include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)