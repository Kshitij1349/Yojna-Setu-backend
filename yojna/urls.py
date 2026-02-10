from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmerViewSet, SchemeViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'farmers', FarmerViewSet, basename='farmer')  
router.register(r'schemes', SchemeViewSet, basename='scheme')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]