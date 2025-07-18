from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView

from .forms import CustomUserCreationForm,  CustomUserChangeForm
from .serializers import ItemsSerializer, UserSerializer, ItemOrdeersSerializer, SignUpSerializer
from .models import Items
from .utils.math_utils import hitung_kuadrat, hitung_regresi_harga

from api.mixins import UserQuerySetMixin
from api.permissions import IsStaffOrOwner

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import generics,status, permissions
from rest_framework.permissions import AllowAny

import logging

logger = logging.getLogger(__name__)

User = get_user_model()

def redirect_login(request):
    return redirect('login')

@login_required
def index(request):
    latest_item_list = Items.objects.order_by('-created')[:5]
    # template = loader.get_template("items/index.html")
    context = {
        'latest_item_list': latest_item_list,
    }
    # return HttpResponse(template.render(context, request))
    return render(request, "items/index.html", context)


def item_detail(request, pk):
    item = get_object_or_404(Items, pk=pk)
    return render(request, "items/detail.html", {'item': item})

class SignupView2(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return Response({'detail': 'Anda sudah login, tidak dapat mendaftar lagi.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

# Create your views here.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login berhasil")
            return redirect(reverse('fixit_frw:item_idx'))  # Ganti dengan halaman tujuan setelah login
        else:
            messages.error(request, "Username atau password salah")
    
    return render(request, "registration/login.html")

# Default sign up using django templates
def authView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form" : form})

class KuadratView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        value = request.data.get('value')
        if value is not None:
            try:
                value = int(value)
                result = hitung_kuadrat(value)
                return Response({'kuadrat': result})
            except (ValueError, TypeError):
                return Response({'error': 'value harus berupa angka'}, status=400)
        return Response({'error': 'value tidak diberikan'}, status=400)

class LinearRegressionPriceView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        try:
            hasil = hitung_regresi_harga()
            return Response({'regression': hasil})
        except ValueError as e:
            return Response({'error': str(e)}, status=400)

# Sign Up from separated client
class SignUpView(generics.ListCreateAPIView):
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
    
# Permission kustom: hanya user staff yang diizinkan
class StaffOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class UsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, StaffOnlyPermission]
    
# get all items
class ItemsView(
                    # StaffEditorPermissionMixin, 
                    UserQuerySetMixin, 
                    generics.ListCreateAPIView
                ):
    parser_classes = [MultiPartParser, FormParser]
    queryset = Items.objects.all().select_related('user')
    permission_classes = [IsStaffOrOwner]
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ItemsSerializer
        return ItemOrdeersSerializer

    
# get detail item
# fixit_frw/views.py
class ItemDetailView(UserQuerySetMixin, generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    lookup_fields = ['pk']
    permission_classes = [IsStaffOrOwner]  # Hanya gunakan satu permission

    def get_queryset(self):
        qs = Items.objects.all().select_related('user')
        return qs

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field):
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ItemsSerializer
        return ItemOrdeersSerializer

    
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsStaffOrOwner]

