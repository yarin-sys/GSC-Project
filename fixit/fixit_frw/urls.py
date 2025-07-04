
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('signup/', views.authView, name="authView"),
    path('signup2/', views.SignupView2.as_view(), name="SignUpView"),
    path("accounts/", include("django.contrib.auth.urls")),
    
    path('users/', views.UsersView.as_view(), name='user-list'),
    path('user/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    
    path("items/", views.ItemsView.as_view(), name="item_list"),
    path("item/<int:pk>", views.ItemDetailView.as_view(), name="item_detail"),

    path("item-idx/",  views.index, name="item_idx"),
    path("item-idx/<int:pk>", views.item_detail, name="item_detail_idx"),
]

urlpatterns = format_suffix_patterns(urlpatterns)