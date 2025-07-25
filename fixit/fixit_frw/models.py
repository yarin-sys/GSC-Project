from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.utils import timezone

from fixit_frw.utils.generator import generate_short_id_from_name, generate_custom_id_with_suffix
import  uuid

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(null=True, blank=True, unique=True, max_length=20)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='user', blank=True, null=True)
    profile_pict = models.ImageField(upload_to='profile/', null=False, blank=False)

    def delete(self, *args, **kwargs):
        if self.profile_pict:
            self.profile_pict.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]
        
class ItemQuerySet(models.QuerySet):
    def search(self, query, user=None):
        lookup = Q(item_name__icontains=query)
        qs = self.filter(lookup)
        
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
            
        return qs

class ItemManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ItemQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)
    
class Items(models.Model):
    class Level(models.IntegerChoices):
        LOW = 1
        MODERATE = 2
        CONSIDERABLE = 3
        DANGEROUS = 4
        EXTREME =5
    
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='items')
    created = models.DateTimeField(auto_now_add=True)
    item_name = models.CharField(max_length=150, db_index=True, default='')
    picture = models.ImageField(upload_to='items/', null=False, blank=False)
    rate = models.IntegerField(default=2, choices=Level.choices)
    deskripsi = models.TextField(blank=False, null=False)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    price_offered = models.BigIntegerField(null=True, blank=True)
    price_final = models.BigIntegerField(null=True, blank=True)
    payment = models.ForeignKey('Payments', on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    fixed = models.BooleanField(default=False, null=False, blank=False)
    
    objects = ItemManager()
    
    class Meta:
        ordering = ['created']
        db_table = 'items'
    
    def __str__(self):
        if self.fixed:
            msg = "Fixed"
        else:
            msg="Processed"
        return f"{self.item_name}({self.user } => {self.created})[{msg}]"
    
    def save(self, *args, **kwargs):
        if not self.address and self.user and self.user.address:
            self.address = self.user.address
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        self.picture.delete(save=False)  # Tambahkan save=False agar tidak error
        super().delete(*args, **kwargs)

class Address(models.Model):
    address_id = models.CharField(max_length=20, primary_key=True, editable=False)
    province = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'address'

    def save(self, *args, **kwargs):
        if not self.address_id:
            self.address_id = generate_custom_id_with_suffix(self.city)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.street + " " + self.city

class Payments(models.Model):
    class Method(models.TextChoices):
        GOPAY = "GOPAY"
        TRANSFER = "TRANSFER"
        COD = "COD"

    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(default="COD", choices=Method.choices)
    amount = models.BigIntegerField(null=True, blank=True)


    class Meta:
        db_table = 'payments'