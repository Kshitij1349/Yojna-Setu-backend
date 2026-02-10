from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from .models import Farmer, Scheme, Notification, WatchLater, WatchHistory
from .serializers import FarmerSerializer, SchemeSerializer, NotificationSerializer, WatchHistorySerializer, WatchLaterSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

class FarmerViewSet(viewsets.ModelViewSet):
    serializer_class = FarmerSerializer
    
    def get_permissions(self):
        if self.action == 'create':  # Registration
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        # Security: Users can only see/edit their own profile
        if self.request.user.is_authenticated:
            return Farmer.objects.filter(id=self.request.user.id)
        return Farmer.objects.none()

class SchemeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SchemeSerializer
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
            # user = self.request.user
            # return Scheme.objects.filter(
            #     is_active=True,
            #     target_districts__contains=user.district
            # )
            return Scheme.objects.filter(is_active=True)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Optimization: Use select_related to avoid N+1 queries
        return Notification.objects.filter(
            farmer=self.request.user
        ).select_related('scheme')
    
    @action(detail=True, methods=['post'])
    def mark_viewed(self, request, pk=None):
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'status': 'notification marked as viewed'})
    


class WatchHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = WatchHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WatchHistory.objects.filter(
            farmer=self.request.user
        ).select_related('scheme').order_by('-last_watched_at')
    
    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        watch_history = self.get_object()
        watch_history.completed = True
        watch_history.last_watched_at = timezone.now()
        watch_history.save()
        return Response({'status': 'marked as completed'})

class WatchLaterViewSet(viewsets.ModelViewSet):
    serializer_class = WatchLaterSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WatchLater.objects.filter(
            farmer=self.request.user
        ).select_related('scheme').order_by('-saved_at')
    
    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)



@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })
    return Response({'error': 'Invalid credentials'}, status=400)
