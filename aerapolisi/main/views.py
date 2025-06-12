import json

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


from .utils import DataMixin
from .forms import ContactForm
from shop.models import Products, OrderInfo, Favourite, FavouriteItem, ProductOffers
from .services import send_smtp_email_message


class MainPageView(FormView):
    template_name = "main/main_page.html"
    form_class = ContactForm
    success_url = reverse_lazy("main")

    def form_valid(self, form, **kwargs):
        """Prepare the data from form for sending an email"""
        user = "Guest"
        if self.request.user.is_authenticated:
            user = self.request.user
        form_data = form.cleaned_data
        name = form_data["name"]
        email_sen = form_data["email"]

        send_smtp_email_message(user, name, email_sen, form_data["message"])

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Main Page"
        return context


@login_required
def updateItem(request):
    data = json.loads(request.body)
    productID = data["productId"]
    action = data["action"]
    product = Products.objects.get(id=productID)

    if action in ("remove", "add"):
        customer = request.user.customer
        favourite, created = Favourite.objects.get_or_create(customer=customer)
        favouriteItem, created = FavouriteItem.objects.get_or_create(
            favourite=favourite, product=product
        )
        if action == "remove":
            favouriteItem.delete()
    elif action in ("approve", "decline"):

        if action == "decline":
            product.delete()
        else:
            product.ontest = False
            product.save()
            ProductOffers.objects.create(
                product=product,
                price=product.price,
                availability=product.quantity,
                owner=product.seller.customer,
            )

    return JsonResponse("Item was changed", safe=False)
