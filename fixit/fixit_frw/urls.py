
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('signup/', views.authView, name="authView"),
    path('signup2/', views.SignUpView.as_view(), name="SignUpView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('api-auth/', include('rest_framework.urls')),
    
    path('users/', views.UserList.as_view(), name='user-list'),
    # path('user/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    
    path("items/", views.ItemsView.as_view(), name="item_list"),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)