from django.urls import path

from .views import BalanceReplenishing, create_checkout_session, \
    payment_successful, payment_cancelled, stripe_webhook


urlpatterns = [
    path("balance_rl", BalanceReplenishing.as_view(), name="balance_rl"),
    path('create-checkout-session/<int:payment_id>', create_checkout_session, name='payment-create'),
    path("payment_successful/", payment_successful, name="payment_successful"),
    path("payment_cancelled", payment_cancelled, name="payment_cancelled"),
    path("webhooks/stripe/", stripe_webhook, name="stripe-webhook")
]