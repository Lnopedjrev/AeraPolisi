from django.conf import settings

import stripe


def get_session_data(payment):
    """Prepares the session data for stripe API"""
    domain_url = "http://127.0.0.1:8000"
    stripe.api_key = settings.STRIPE_SECRET_KEY
    success_url = domain_url + "/transactions/payment_successful"
    cancel_url = domain_url + "/transactions/payment_cancelled"

    session_data = {
        "success_url": success_url,
        "cancel_url": cancel_url,
        "mode": "payment",
        "line_items": [],
        "metadata": {"payment_id": payment.id},
    }

    unit_converted = int(payment.value * 100)

    session_data["line_items"].append(
        {
            "price_data": {
                "unit_amount": unit_converted,
                "currency": "usd",
                "product_data": {
                    "name": "Replensih account",
                },
            },
            "quantity": 1,
        }
    )
    return session_data
