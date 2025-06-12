from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from typing import Any

from logapp.models import User
from .models import (
    ProductOffers,
    ProductsGallery,
    Products,
    OrderInfo,
    ShippingAdress,
    OrderRequests,
)
from main.utils import DataMixin
from main.services import is_htmx
from .forms import (
    SupposeProductForm,
    FilterProductForm,
    ProductPurchaseForm,
    ShippingChangeForm,
)


class Shop(DataMixin, ListView):
    paginate_by = 9
    model = ProductOffers
    template_name = "shop/shop-main.html"

    def get_template_names(self):
        """Check if the loading page hast htmx"""
        if is_htmx(self.request):
            return "shop/shop-main__search-results.html"
        else:
            return "shop/shop-main.html"

    def get_queryset(self) -> QuerySet[Any]:

        new_queryset = (
            ProductOffers.objects.filter(product__ontest=False, is_active=True)
            .select_related("product", "owner", "product__seller", "owner__user")
            .prefetch_related("product__productsgallery_set")
        )

        if is_htmx(self.request):
            params = self.request.GET

            filter_name = params.get("search-product", "")
            new_queryset = new_queryset.filter(product__name__icontains=filter_name)

            serv_html = params.get("is_service", None)
            if serv_html is not None:
                serv_html = True if serv_html == "Service" else False
                new_queryset = new_queryset.filter(product__service=serv_html)

            min_range = params.get("price-min")
            max_range = params.get("price-max")
            if min_range is not None and max_range is not None:
                new_queryset = new_queryset.filter(
                    product__price__gte=min_range, product__price__lte=max_range
                )

            categories = self.request.GET.getlist("categories")
            if categories:
                new_queryset = new_queryset.filter(
                    product__categories__name__in=categories
                )

            seller_name = params.get("seller-search", None)
            if seller_name is not None:
                seller_inf = ""
                try:
                    seller_inf = User.objects.get(username=seller_name)
                    new_queryset = new_queryset.filter(seller=seller_inf)
                except Exception as e:
                    print(e)
        return new_queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        req_user = self.request.user
        fav_list = (
            req_user.customer.get_favourite_products_list()
            if req_user.is_authenticated
            else []
        )
        view_context = dict(
            title="Shop",
            fav_list=fav_list,
            form=FilterProductForm,
            paginate_except=True,
        )
        return {**context, **view_context}


def favourite(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        fav_items = customer.get_favourite_products_list
    else:
        fav_items = []

    context = {"items": fav_items}
    return render(request, "shop/favourite-page.html", context)


class SupposeProduct(LoginRequiredMixin, DataMixin, CreateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    form_class = SupposeProductForm
    template_name = "shop/product-create_page.html"
    login_url = reverse_lazy("logpage")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Product"
        return context

    def form_valid(self, form):
        user = self.request.user
        data = form.cleaned_data
        product, created = Products.objects.get_or_create(
            seller=user,
            name=data["name"],
            description=data["description"],
            quantity=data["quantity"],
            price=data["price"],
            service=data["service"],
            ontest=True,
        )
        for category in data["categories"]:
            product.categories.add(category)
        for image in data["images"]:
            ProductsGallery.objects.create(image=image, product=product)
        return redirect("shop")


class ProductShow(UserPassesTestMixin, DataMixin, DetailView):
    model = Products
    template_name = "shop/product-page.html"
    context_object_name = "product"
    pk_url_kwarg = "id"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context["product"]
        images = ProductsGallery.objects.filter(product=product).select_related(
            "product"
        )
        visitor = self.request.user
        seller = product.seller
        if visitor.is_authenticated and visitor != seller:
            # check if the product is in the favourite list
            fav_list = visitor.consumer.get_favourite_products_list()
        else:
            fav_list = []
        user_context = dict(
            title=product,
            images=images,
            first_image=images[0],
            fav_list=fav_list,
            seller=seller,
        )
        return {**context, **self.get_user_context(**user_context)}

    # consider using roles or something
    def test_func(self, **kwargs):
        """Tests if the product has not been managed
        by the administration yet"""
        product = self.get_object()
        return not product.ontest or self.request.user.is_superuser


# Fully refactor this class
class ProductPurchase(UserPassesTestMixin, DataMixin, FormView):

    template_name = "shop/product-purchase.html"
    form_class = ProductPurchaseForm
    model = ShippingAdress
    success_url = reverse_lazy("main")

    def get_success_url(self):
        return reverse("main")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.offer.product
        title = str(product.name) + " purchase"
        product_image = product.productsgallery_set.first()
        view_context = dict(
            title=title, image=product_image, product=product, offer=self.offer
        )
        return {**context, **view_context}

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)

    def form_valid(self, form, **kwargs):
        offer = self.offer
        owner = offer.owner.user
        quantity = form.cleaned_data["number"]
        total_price = offer.price * quantity

        if offer.availability < quantity < 0:
            error_text = "Number can't exceed the current availability"
            form.add_error("number", error_text)
            return self.form_invalid(form)

        if total_price > self.request.user.balance:
            form.add_error(None, "You don't own enough money to purchase it")
            return self.form_invalid(form)

        else:
            visitor = self.request_user
            customer = visitor.customer
            with transaction.atomic():
                offer.availability = offer.availability - quantity
                visitor.balance = visitor.balance - total_price
                owner.balance = owner.balance + total_price
            owner.save()
            visitor.save()
            offer.save()

            product = offer.product
            new_offer, created = ProductOffers.objects.get_or_create(
                owner=customer, product=product
            )
            new_offer.availability += quantity
            new_offer.save()

            order = OrderInfo.objects.create(
                payee=customer, quantity=quantity, offer=new_offer
            )
            order.save()
            if not offer.product.service:
                ship = ShippingAdress.objects.create(
                    order=order,
                    address=form.cleaned_data["address"],
                    city=form.cleaned_data["city"],
                    state=form.cleaned_data["state"],
                )
                ship.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        """Checks the request user is authenticated
        and not productoffer's seller/owner"""
        offer_id = self.kwargs["id"]
        self.offer = ProductOffers.objects.get(id=offer_id)
        self.request_user = self.request.user
        if not self.request_user.is_authenticated:
            return False
        offer = self.offer
        first_cond = self.request_user != offer.product.seller
        second_cond = self.request_user != offer.owner.user
        return first_cond and second_cond


class ProductCheckout(UserPassesTestMixin, DataMixin, FormView):
    form_class = ShippingChangeForm
    template_name = "shop/product_checkout-page.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("shop")

    def form_valid(self, form, **kwargs):
        f_data = form.cleaned_data
        number = f_data["number"]
        offer = ProductOffers.objects.get(id=self.kwargs["id"])
        if number > offer.availability:
            return self.form_invalid(form)

        customer = self.request.user.customer
        last_order = OrderInfo.objects.filter(offer=offer, payee=customer).last()

        ship = None
        if not offer.product.service:
            ship, created = ShippingAdress.objects.get_or_create(
                address=f_data["address"],
                order=last_order,
                city=f_data["city"],
                state=f_data["state"],
                zipcode=f_data["zipcode"],
            )
        with transaction.atomic():
            orderreq, created = OrderRequests.objects.get_or_create(
                shipping=ship, last_order=last_order
            )
            orderreq.number += number
            orderreq.save()
            offer.availability -= number
            offer.save()
        return HttpResponseRedirect(f"/chat_rooms/{offer.product.seller}")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        offer = ProductOffers.objects.get(id=self.kwargs["id"])
        ship = list()
        customer = self.request.user.customer
        if not offer.product.service:
            last_order = OrderInfo.objects.filter(offer=offer, payee=customer).last()
            ship = ShippingAdress.objects.filter(order=last_order).last()
        title = f"Check Out Offer-{offer.id}"
        view_context = dict(title=title, ship=ship, offer=offer)
        return {**context, **view_context}

    def test_func(self):
        offer = ProductOffers.objects.get(id=self.kwargs["id"])
        if offer.availability <= 0:
            return False
        visitor_customer = self.request.user.customer
        return offer.owner == visitor_customer and not offer.is_active
