from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.core.mail import EmailMessage
from .utils import DataMixin
from django.conf import settings
from django.http import JsonResponse

import json

from .forms import ContactForm
from shop.models import Products, OrderInfo
from .services import regulate_favourite, regulate_new_product


class MainPageView(DataMixin, FormView):
    template_name = "main/main_page.html"
    form_class = ContactForm
    success_url = reverse_lazy('main')

    def form_valid(self, form, **kwargs):
        """Prepare the data from form for sending an email"""
        user = 'Guest'
        if self.request.user.is_authenticated:
            user = self.request.user
        name = form.cleaned_data['name']
        email_sen = form.cleaned_data['email']
        email_rec = settings.EMAIL_HOST_USER
        message = 'From' + str(user) + form.cleaned_data['message']

        EmailMessage(
            subject="Contact Form Submission from {}".format(name),
            body=message,
            from_email=email_sen,
            to=[email_rec,],
            headers=[],
            reply_to=[email_sen]
        ).send()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Main Page"
        return context


def updateItem(request):
    data = json.loads(request.body)
    productID = data['productId']
    action = data['action']
    product = Products.objects.get(id=productID)

    if action in ("remove", "add"):
        customer = request.user.customer
        regulate_favourite(product, action, customer)
    elif action in ("approve", "decline"):
        regulate_new_product(product, action)

    return JsonResponse('Item was changed', safe=False)


def updateOrder(request):
    data = json.loads(request.body)
    orderID = data['orderID']
    action = data['action']

    if action == 'complete':
        order = OrderInfo.objects.get(id=orderID)
        order.comlete = True
        order.save()

    return JsonResponse('Order was completed', safe=False)
