from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Items

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'address','phone', 'profile_pict', 'email']  

class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'profile_pict', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
        
# Serializer for fixer
class ItemsSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(read_only=True)
    price_offered = serializers.ReadOnlyField()
    owner = UserSerializer(source='user', read_only=True)
    class Meta:
        model = Items
        fields = ['id','created', 'item_name', 'owner','rate', 'picture',
                  'deskripsi', 'pick_address', 'price_offered','price_final' ,'fixed']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_price_offered(self, value):
        if value < 0:
            raise serializers.ValidationError("price offered must be grather than 0")
        return value
    
#Serializer for user
class ItemOrdeersSerializer(serializers.ModelSerializer):
    price_final  = serializers.ReadOnlyField()
    fixed = serializers.ReadOnlyField()
    class Meta:
        model = Items
        fields = ['id','created', 'item_name', 'picture', 'rate', 
                  'deskripsi', 'pick_address', 'price_offered','price_final' ,'fixed']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_price_offered(self, value):
        if value < 0:
            raise serializers.ValidationError("price_offered must be grather than 0")
        return value
    
            
    