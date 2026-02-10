from rest_framework import serializers
from .models import Farmer, Scheme, Notification, WatchLater, WatchHistory

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['id', 'username', 'email', 'password', 'phone', 'district', 'village_taluka']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        # Use create_user to properly hash the password
        user = Farmer.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone'],
            district=validated_data['district'],
            village_taluka=validated_data['village_taluka']
        )
        return user

class SchemeSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Scheme
        fields = '__all__'

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
        return None

class NotificationSerializer(serializers.ModelSerializer):
    scheme = SchemeSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'


class WatchHistorySerializer(serializers.ModelSerializer):
    scheme = SchemeSerializer(read_only=True)
    scheme_id = serializers.PrimaryKeyRelatedField(
        queryset=Scheme.objects.all(), 
        source='scheme', 
        write_only=True
    )
    
    class Meta:
        model = WatchHistory
        fields = ['id', 'scheme', 'scheme_id', 'started_at', 'last_watched_at', 
                  'completed', 'watch_duration_seconds']
        read_only_fields = ['started_at', 'last_watched_at']

class WatchLaterSerializer(serializers.ModelSerializer):
    scheme = SchemeSerializer(read_only=True)
    scheme_id = serializers.PrimaryKeyRelatedField(
        queryset=Scheme.objects.all(), 
        source='scheme', 
        write_only=True
    )
    
    class Meta:
        model = WatchLater
        fields = ['id', 'scheme', 'scheme_id', 'saved_at']
        read_only_fields = ['saved_at']