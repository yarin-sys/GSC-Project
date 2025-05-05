from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Items

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'address','phone', 'profile_pict']  
        
class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['user','created', 'item_name', 'picture', 'rate', 'deskripsi', 'pick_address', 'price_offered', 'price_final']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_price_offered(self, value):
        if value <= 0:
            raise serializers.ValidationError("price_offered must be grather than 0")
        return value
        
    