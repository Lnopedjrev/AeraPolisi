from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.conf import settings
from django.shortcuts import get_object_or_404

import stripe
import stripe.error

from .models import UserPayment
from logapp.utils import DataMixin
from .forms import TransactionInfoForm
from .services import get_session_data


STRIPE_PUBL = settings.STRIPE_PUBLISHABLE_KEY
STRIPE_SECRET = settings.STRIPE_SECRET_KEY


class BalanceReplenishing(CreateView, LoginRequiredMixin, DataMixin):
    template_name = "transactions/balance_replenish.html"
    form_class = TransactionInfoForm
    login_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Transaction execute"
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        userP = UserPayment.objects.create(
            user=self.request.user, value=data["value"], payment_bool=False
        )
        userP.save()

        return redirect("payment-create", payment_id=userP.pk)

    def form_invalid(self, form):
        return super().form_invalid(form)


@csrf_exempt
def create_checkout_session(request, payment_id):
    payment = UserPayment.objects.get(id=payment_id)

    try:
        session_data = get_session_data(payment)
        checkout_session = stripe.checkout.Session.create(**session_data)
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return JsonResponse({"error": str(e)})


def payment_successful(request):
    return render(request, "transactions/payment_successful.html")


def payment_cancelled(request):
    return render(request, "transactions/payment_cancelled.html")


@csrf_exempt
def stripe_webhook(request):
    data = request.body
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(data, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        payment_id = event["data"]["object"]["metadata"]["payment_id"]
        payment = get_object_or_404(UserPayment, id=payment_id)
        with transaction.atomic():
            payment.user.balance += payment.value
            payment.user.save()
            payment.payment_bool = True
            payment.save()

    return HttpResponse(status=200)
