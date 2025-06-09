from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView, # Opcional: para verificar un token sin refrescarlo
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('manuals.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Generar Access y Refresh Token
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Refrescar Access Token
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)