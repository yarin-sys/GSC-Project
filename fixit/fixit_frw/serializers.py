
from .models import Items, Address, Payments
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
        fields = ['address_id','province', 'city','street']
        read_only_fields = ['address_id']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['payment_id', 'method', 'amount', 'date']
        read_only_fields = ['payment_id', 'date']

class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    # profile_pict = serializers.ImageField(required=True)

    address_data = AddressSerializer(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'profile_pict', 'password1', 'password2', 'address_data']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'phone': {'required': True},
            'address_data': {'required': True},
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
        address_data = validated_data.pop('address_data')

        # Make address data first
        address = Address.objects.create(**address_data)

        # Buat user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            phone=validated_data.get('phone'),
            address=address,
            profile_pict=validated_data.get('profile_pict')
        )
        return user
        
# Serializer for fixer
class ItemsSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(read_only=True)
    price_offered = serializers.ReadOnlyField()
    owner = UserSerializer(source='user', read_only=True)

    # payment
    payment_data = PaymentSerializer(read_only=True, required=False, allow_null=True)
    payment = PaymentSerializer(read_only=True)

    # address
    address_data = AddressSerializer(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Items
        fields = ['id','created', 'item_name', 'owner','rate', 'picture',
                  'deskripsi', 'address_data', 'address', 'price_offered','price_final' , 'payment_data', 'payment','fixed']

    def create(self, validated_data):
        payment_data = validated_data.pop('payment_data', None)
        address_data = validated_data.pop('address_data', None)
        user = self.context['request'].user
        validated_data['user'] = user

        # Buat item terlebih dahulu
        item = super().create(validated_data)

        return item

    def update(self, instance, validated_data):
        payment_data = validated_data.pop('payment_data', None)
        address_data = validated_data.pop('address_data', None)

        # Update item
        item = super().update(instance, validated_data)

        return item
    
    def validate_price_offered(self, value):
        if value < 0:
            raise serializers.ValidationError("price offered must be grather than 0")
        return value
    
#Serializer for user
class ItemOrdeersSerializer(serializers.ModelSerializer):
    price_final  = serializers.ReadOnlyField()
    fixed = serializers.ReadOnlyField()

    # payment
    payment_data = PaymentSerializer(write_only=True, required=False, allow_null=True)
    payment = PaymentSerializer(read_only=True)
    # picture =  serializers.ImageField(required=False, allow_null=True)

    # address
    address_data = AddressSerializer(write_only=True, required=False, allow_null=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Items
        fields = ['id','created', 'item_name', 'picture', 'rate', 
                  'deskripsi', 'price_offered','price_final', 'address_data' ,'address', 'payment_data', 'payment' ,'fixed']
        
    def create(self, validated_data):
        payment_data = validated_data.pop('payment_data', None)
        address_data = validated_data.pop('address_data', None)
        user = self.context['request'].user
        validated_data['user'] = user

        # Buat item terlebih dahulu
        item = super().create(validated_data)

        # Jika ada payment_data, buat payment
        if payment_data:
            payment = Payments.objects.create(**payment_data)
            item.payment = payment
            item.save()

        if address_data:
            address = Address.objects.create(**address_data)
            item.address = address
            item.save()

        return item

    def update(self, instance, validated_data):
        payment_data = validated_data.pop('payment_data', None)
        address_data = validated_data.pop('address_data', None)

        # Update item
        item = super().update(instance, validated_data)

        # Handle payment update
        if payment_data:
            if item.payment:
                # Update payment yang sudah ada
                for key, value in payment_data.items():
                    setattr(item.payment, key, value)
                item.payment.save()
            else:
                # Buat payment baru jika belum ada
                payment = Payments.objects.create(**payment_data)
                item.payment = payment
                item.save()

        if address_data:
            if item.address:
                # update address yang ada
                for key, value in address_data.items():
                    setattr(item.address, key, value)
                item.address.save()
            else:
                address = Address.objects.create(**address_data)
                item.address = address
                item.save()

        return item

    def validate(self, attrs):
        price_final = self.instance.price_final if self.instance else None
        payment_data = attrs.get('payment_data')

        if price_final is not None and payment_data:
            amount = payment_data.get('amount', 0)
            if amount < price_final:
                raise serializers.ValidationError({
                    'payment_data': {
                        'amount': [f"Jumlah pembayaran tidak boleh kurang dari price_final {price_final}."]
                    }
                })
            elif amount > price_final:
                raise serializers.ValidationError({
                    'payment_data': {
                        'amount': [f"Jumlah pembayaran lebih dari price_final {price_final}."]
                    }
                })

        return attrs
    
    def validate_price_offered(self, value):
        if value < 0:
            raise serializers.ValidationError("price offered must be greater than 0")

        return value
    
            
    