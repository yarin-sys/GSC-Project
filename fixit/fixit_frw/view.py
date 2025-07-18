from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from api.mixins import UserQuerySetMixin
from fixit_frw.models import Items


class IndexView(LoginRequiredMixin, UserQuerySetMixin, ListView):
    model = Items
    template_name = "items/index.html"
    context_object_name = 'latest_item_list'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().order_by('-created')
