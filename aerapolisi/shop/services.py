from django.db import transaction

from .models import (Favourite, FavouriteItem, Products,
                     ProductsGallery, OrderInfo, ProductOffers)


def get_favourite_list(customer):
    """Returns request user's favourite product list"""
    favouriteproduct, created = (Favourite
                                 .objects
                                 .get_or_create(customer=customer))
    fav_items = (FavouriteItem
                 .objects
                 .filter(favourite=favouriteproduct)
                 .select_related('product', 'product__seller')
                 .prefetch_related('product__productsgallery_set'))
    fav_list = [i.product for i in fav_items]
    return fav_list


def create_new_product(user, form_data):
    '''Creates new_product and attaches images to it'''
    product, created = (Products
                        .objects
                        .get_or_create(seller=user,
                                       name=form_data['name'],
                                       description=form_data['description'],
                                       quantity=form_data['quantity'],
                                       price=form_data['price'],
                                       service=form_data['service'],
                                       ontest=True))
    for category in form_data['categories']:
        product.categories.add(category)
    for image in form_data['images']:
        product_image, created = (ProductsGallery
                                  .objects
                                  .get_or_create(
                                        image=image,
                                        product=product))


def purchase_offer(quantity, total_price, offer, visitor):
    """Process the transaction, creates new offer, returns order for record"""
    customer = visitor.customer
    owner_user = offer.owner.user
    with transaction.atomic():
        offer.availability = offer.availability - quantity
        visitor.balance = visitor.balance - total_price
        owner_user.balance = owner_user.balance + total_price
    owner_user.save()
    visitor.save()
    offer.product.save()

    product = offer.product
    new_offer, created = (ProductOffers
                          .objects
                          .get_or_create(owner=customer,
                                         product=product))
    new_offer.availability += quantity
    new_offer.save()

    order = OrderInfo.objects.create(payee=customer,
                                     quantity=quantity,
                                     offer=new_offer)
    order.save()
    return order
