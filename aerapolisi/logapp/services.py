
from shop.models import Favourite, Customer, ProductOffers
from django.db.models import Q


def create_new_customer(user):
    """Creating new customer"""
    customer_name = user.username + '_customer'
    customer, created = (Customer
                         .objects
                         .get_or_create(user=user,
                                        name=customer_name,
                                        email=user.email))
    Favourite.objects.create(customer=customer)


def get_all_user_products(user):
    """Return all the products user either possesses or created"""
    productoffers = (ProductOffers
                     .objects
                     .filter(Q(owner=user.customer)
                             | Q(product__seller=user))
                     .filter(availability__gt=0)
                     .select_related('product', 'product__seller')
                     .prefetch_related('product__productsgallery_set'))

    own_products = list(set([a.product for a in productoffers]))
    return own_products
