from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmerViewSet, SchemeViewSet, NotificationViewSet, WatchHistoryViewSet, WatchLaterViewSet
from .views import login_view

router = DefaultRouter()
router.register(r'farmers', FarmerViewSet, basename='farmer')  
router.register(r'schemes', SchemeViewSet, basename='scheme')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'watch-history', WatchHistoryViewSet, basename='watchhistory')
router.register(r'watch-later', WatchLaterViewSet, basename='watchlater')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
]