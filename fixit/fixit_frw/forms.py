from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    profile_pict = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ("username", "email", "phone","profile_pict" ,"address_id", "password1", "password2")
        
class  CustomUserChangeForm(UserCreationForm):
    profile_pict = forms.ImageField(required=False)
    password1 = None #hiding password1
    password2 = None #hiding password2
    class Meta:
        model = User
        fields = ("username", "email", "phone","profile_pict" ,"address_id")