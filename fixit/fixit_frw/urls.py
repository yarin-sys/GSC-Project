
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

import fixit_frw.view
from . import views

app_name = 'fixit_frw'
urlpatterns = [

    path('login/', views.user_login, name='login'),

    path('signup/', views.authView, name="authView"),
    path('signup2/', views.SignupView2.as_view(), name="SignUpView"),
    path("accounts/", include("django.contrib.auth.urls")),
    
    path('users/', views.UsersView.as_view(), name='user-list'),
    path('user/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    
    path("items/", views.ItemsView.as_view(), name="item_list"),
    path("item/<int:pk>", views.ItemDetailView.as_view(), name="item_detail"),

    path("item-idx/", fixit_frw.view.IndexView.as_view(), name="item_idx"),
    path("item-idx/<int:pk>", views.item_detail, name="item_detail_idx"),

    path("kuadrat/", views.KuadratView.as_view(), name="kuadrat"),

    path('analitic/price/', views.LinearRegressionPriceView.as_view(), name="analitic_price"),
]

urlpatterns = format_suffix_patterns(urlpatterns)