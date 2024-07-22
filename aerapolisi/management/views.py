from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.utils import DataMixin
from shop.models import Products


class ProductsOnTestList(DataMixin, ListView, LoginRequiredMixin):
    paginate_by = 3
    model = Products
    template_name = 'management/managing-products.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(ontest=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Managing Products")
        return dict(list(context.items()) + list(c_def.items()))

    def test_func(self):
        return self.request.user.has_perm()
