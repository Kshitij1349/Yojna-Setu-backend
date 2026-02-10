from rest_framework import serializers
from .models import Farmer, Scheme, Notification

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
    class Meta:
        model = Scheme
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    scheme = SchemeSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'