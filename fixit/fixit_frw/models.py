from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(null=True, blank=True,unique=True, max_length=20)
    address = models.TextField()
    profile_pict = models.ImageField(upload_to='profile/', null=False, blank=False)
    
    def delete(self, *args, **kwargs):
        self.picture.delete(save=False)  # Tambahkan save=False agar tidak error
        super().delete(*args, **kwargs)
    
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
    pick_address = models.TextField(null=True, blank=True)
    price_offered = models.BigIntegerField(null=True, blank=True)
    price_final = models.BigIntegerField(null=True, blank=True)
    fixed = models.BooleanField(default=False, null=False, blank=False)
    
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
        if not self.pick_address and self.user:
            self.pick_address = self.user.address
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        self.picture.delete(save=False)  # Tambahkan save=False agar tidak error
        super().delete(*args, **kwargs)
        