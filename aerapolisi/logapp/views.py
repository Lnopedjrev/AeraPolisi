from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.db.models import Q
from shop.models import Customer, Favourite

import json

from logapp.models import User
from shop.models import ProductOffers, Products, OrderRequests, OrderInfo
from .forms import (
    LoginUserForm,
    RegisterUserForm,
    EditUserForm,
    EditProductForm,
    EditOfferForm,
)


class LoginUser(UserPassesTestMixin, LoginView):
    form_class = LoginUserForm
    template_name = "logapp/log_page.html"
    login_url = reverse_lazy("main")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Log in Page"
        return context

    def get_success_url(self):
        return reverse_lazy("main")

    def test_func(self):
        return not self.request.user.is_authenticated


class RegisterUser(UserPassesTestMixin, CreateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    form_class = RegisterUserForm
    template_name = "logapp/register_page.html"
    success_url = reverse_lazy("main")
    login_url = reverse_lazy("main")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Registration page"
        return context

    def form_valid(self, form):
        """Creating new customer and attaching favourite"""
        user = form.save()
        customer_name = user.username + "_customer"
        customer, created = Customer.objects.get_or_create(
            user=user, name=customer_name, email=user.email
        )
        Favourite.objects.create(customer=customer)

        backend = "django.contrib.auth.backends.ModelBackend"
        login(self.request, user, backend=backend)
        return redirect("main")

    def test_func(self):
        return not self.request.user.is_authenticated


def logoutuser(request):
    logout(request)
    return redirect("main")


class UserShow(DetailView):
    model = User
    template_name = "logapp/profile_page.html"
    context_object_name = "page_user"
    slug_url_kwarg = "username"
    slug_field = "username"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_style = ""
        visitor = self.request.user
        user = context["page_user"]
        if user != visitor:
            extra_style = "hidden"

        productoffers = (
            ProductOffers.objects.filter(
                Q(owner=self.customer) | Q(product__seller=self)
            )
            .filter(availability__gt=0)
            .select_related("product", "product__seller")
            .prefetch_related("product__productsgallery_set")
        )

        own_products = list(set([a.product for a in productoffers]))
        view_context = dict(title=user, extra_style=extra_style, products=own_products)
        return {**context, **view_context}


class EditUser(UserPassesTestMixin, UpdateView):
    model = User
    form_class = EditUserForm
    template_name = "logapp/profile_edit_page.html"
    context_object_name = "page_user"
    slug_url_kwarg = "username"
    slug_field = "username"
    redirect_field_name = "main"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Change profile"
        return context

    def test_func(self):
        """Tests if the request user is the user, whose page is changed"""
        page_user = User.objects.get(username=self.kwargs["username"])
        return page_user == page_user


class ProductsMaintain(LoginRequiredMixin, ListView):
    model = ProductOffers
    template_name = "logapp/user_warehouse.html"

    def get_queryset(self):
        user = self.request.user
        productoffer_list = (
            ProductOffers.objects.filter(
                Q(owner=user.customer) | Q(product__seller=user)
            )
            .filter(availability__gt=0)
            .select_related("product", "product__seller")
            .prefetch_related("product__productsgallery_set")
        )
        return productoffer_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        ln_rl = OrderRequests.objects.filter(
            last_order__offer__product__seller=user, last_order__complete=False
        ).count()
        title = str(user).capitalize() + " maintains products"
        view_context = dict(title=title, ln_req_l=ln_rl)
        return {**context, **view_context}


class EditProduct(UserPassesTestMixin, UpdateView):
    model = Products
    form_class = EditProductForm
    template_name = "logapp/edit_product.html"
    context_object_name = "edit"
    redirect_field_name = "main"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        product = self.product
        return product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Adjust Product"
        return context

    def test_func(self):
        """Test if the request user is the seller of the product"""
        product_id = self.kwargs.get(self.pk_url_kwarg)
        self.product = Products.objects.get(id=product_id)
        return self.request.user == self.product.seller

    def form_invalid(self, form: EditProductForm) -> HttpResponse:
        print(form.errors)
        return super().form_invalid(form)


class EditOffer(UpdateView):
    model = ProductOffers
    form_class = EditOfferForm
    template_name = "logapp/edit_offer.html"
    context_object_name = "offer"
    pk_url_kwarg = "id"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Adjust offer"
        return context

    def test_func(self):
        offer = self.get_object()
        return self.request.user == offer.owner.user

    def get_success_url(self) -> str:
        return reverse("products-maintain")


class RequestsCheck(ListView, LoginRequiredMixin):
    template_name = "logapp/user_requests.html"
    model = OrderRequests
    paginate_by = 5

    def get_queryset(self):
        req_user = self.request.user
        object_list = OrderRequests.objects.filter(
            last_order__offer__product__seller=req_user, last_order__complete=False
        )
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Requests to {self.request.user}"
        return context


def updateOrder(request):
    data = json.loads(request.body)
    orderID = data["orderId"]
    action = data["action"]

    if action == "complete":
        order = OrderInfo.objects.get(id=orderID)
        order.complete = True
        order.save()

    return JsonResponse("Order was completed", safe=False)
