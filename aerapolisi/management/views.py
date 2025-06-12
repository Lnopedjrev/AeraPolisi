from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from shop.models import Products


class ProductsOnTestList(ListView, LoginRequiredMixin):
    paginate_by = 3
    model = Products
    template_name = "management/managing-products.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(ontest=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        view_context = dict(title="Managing Products")
        return {**context, **view_context}

    def test_func(self):
        return self.request.user.has_perm()
