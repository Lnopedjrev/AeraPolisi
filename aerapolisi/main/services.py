from shop.models import Favourite, FavouriteItem, ProductOffers
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import EmailMessage


def paginate(request, qers, limit=3):
    paginated_qers = Paginator(qers, limit)
    page_num = request.GET.get("page")
    return paginated_qers.get_page(page_num)


def is_htmx(request, boost_check=True):
    hx_boost = request.headers.get("Hx-Boosted")
    hx_request = request.headers.get("Hx-Request")

    if boost_check and hx_boost:
        return False

    elif boost_check and not hx_boost and hx_request:
        return True


def send_smtp_email_message(user, name, recipient_email, message):
    # take the email sending logic into services
    sender_email = settings.EMAIL_HOST_USER
    message = f"From {user} {message}"

    email_message = EmailMessage(
        subject="Contact Form Submission from {} by email {}".format(
            name, sender_email
        ),
        body=message,
        from_email=sender_email,
        to=[
            recipient_email,
        ],
        headers=[],
        reply_to=[sender_email],
    )

    email_message.send()
