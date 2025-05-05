from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm,  CustomUserChangeForm
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.mixins import StaffEditorPermissionMixin, UserQuerySetMixin
from rest_framework import generics
from .serializers import ItemsSerializer, UserSerializer, ItemOrdeersSerializer
from .models import Items

User = get_user_model()

# Create your views here.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login berhasil")
            return redirect("http://localhost:8000/")  # Ganti dengan halaman tujuan setelah login
        else:
            messages.error(request, "Username atau password salah")
    
    return render(request, "login.html")

# Default sign up using django templates
def authView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('http://localhost:8000/accounts/login/')
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form" : form})

# Sign Up from separated client
class SignUpView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        form_fields = {field.name: field.label for field in form}  # Optional: return field names & labels
        return Response({'form_fields': form_fields})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.data, request.FILES)
        if form.is_valid():
            user = form.save()
            return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        form = CustomUserChangeForm(request.data, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return Response({"message": "Profil berhasil diperbarui"}, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        form = CustomUserChangeForm(request.data, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return Response({"message": "Profil diperbarui (parsial)"})
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ItemsView(  StaffEditorPermissionMixin, 
                  UserQuerySetMixin, 
                  generics.ListCreateAPIView
                  ):
    
    queryset = Items.objects.all().select_related('user')
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ItemsSerializer
        return ItemOrdeersSerializer
    
class ItemDetailView(   StaffEditorPermissionMixin, 
                        UserQuerySetMixin, 
                        generics.RetrieveUpdateDestroyAPIView
                    ):
    # queryset = Items.objects.all().select_related('user')
    lookup_fields = ['pk']
    
    def get_queryset(self):
        qs = Items.objects.all().select_related('user')
        return qs
    
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field): # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ItemsSerializer
        return ItemOrdeersSerializer

    
class UserList(StaffEditorPermissionMixin, 
               generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer