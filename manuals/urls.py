# manuals/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ManualViewSet, ProcedureViewSet, DocumentFileViewSet, UserRegisterView, UserProfileView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'manuals', ManualViewSet)
router.register(r'procedures', ProcedureViewSet)
router.register(r'files', DocumentFileViewSet)


urlpatterns = [
        path('', include(router.urls)),
        path('register/', UserRegisterView.as_view(), name='register'),
        path('profile/', UserProfileView.as_view(), name='user-profile'),
]