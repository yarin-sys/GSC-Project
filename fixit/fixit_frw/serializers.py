
from .models import Items, Address
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'address_id','phone', 'profile_pict', 'email']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['province', 'city','street']

class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address_id', 'profile_pict', 'password1', 'password2']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'phone': {'required': True},
            'address_id': {'required': True},
            'profile_pict': {'required': True},
        }

    def validate_email(self, value):
        """Validasi email harus unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email sudah terdaftar.")
        return value

    def validate_phone(self, value):
        """Validasi phone harus unique jika diisi"""
        if value and User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Nomor telepon sudah terdaftar.")
        return value

    def validate(self, attrs):
        """Validasi password1 dan password2 harus sama"""
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Password tidak cocok.")
        return attrs

    def create(self, validated_data):
        # Hapus password2 karena tidak perlu disimpan
        validated_data.pop('password2', None)
        password = validated_data.pop('password1')

        # Buat user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            phone=validated_data.get('phone'),
            address_id=validated_data.get('address_id'),
            profile_pict=validated_data.get('profile_pict')
        )
        return user
        
# Serializer for fixer
class ItemsSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(read_only=True)
    price_offered = serializers.ReadOnlyField()
    owner = UserSerializer(source='user', read_only=True)
    class Meta:
        model = Items
        fields = ['id','created', 'item_name', 'owner','rate', 'picture',
                  'deskripsi', 'address_id', 'price_offered','price_final' ,'fixed']
        
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
                  'deskripsi', 'address_id', 'price_offered','price_final' ,'fixed']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_price_offered(self, value):
        if value < 0:
            raise serializers.ValidationError("price_offered must be greter than 0")
        return value
    
            
    