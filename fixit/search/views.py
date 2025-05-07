# from django.shortcuts import render

from rest_framework import generics
from fixit_frw.models import Items
from fixit_frw.serializers import ItemOrdeersSerializer

from api.mixins import UserQuerySetMixin

class SearchItemListView(
                            generics.ListAPIView,
                            UserQuerySetMixin
                        ):
    queryset = Items.objects.all()
    serializer_class = ItemOrdeersSerializer
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Items.objects.none()
        
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = qs.search(q, user=user)
        
        return results