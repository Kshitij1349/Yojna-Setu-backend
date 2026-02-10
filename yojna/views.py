from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from .models import Farmer, Scheme, Notification
from .serializers import FarmerSerializer, SchemeSerializer, NotificationSerializer

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
        # Filter schemes by user's district
        user = self.request.user
        return Scheme.objects.filter(
            is_active=True,
            target_districts__contains=user.district
        )

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