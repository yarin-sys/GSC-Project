from django .urls import path

from . import views

urlpatterns = [
    path('item/', views.SearchItemListView.as_view(), name='item-search')
]