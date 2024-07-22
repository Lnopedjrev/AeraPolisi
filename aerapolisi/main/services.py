from shop.models import Favourite, FavouriteItem, ProductOffers


def regulate_favourite(product, action, customer):
    """Adds or removes product from the customer's favourite list"""
    favourite, created = Favourite.objects.get_or_create(customer=customer)
    favouriteItem, created = (FavouriteItem
                              .objects
                              .get_or_create(favourite=favourite,
                                             product=product))
    if action == 'remove':
        favouriteItem.delete()


def regulate_new_product(product, action):
    """Creates an initial offer based on product instance,
        if declined - deletes the product"""
    if action == "decline":
        product.delete()
    else:
        product.ontest = False
        product.save()
        productoffer, created = (ProductOffers
                                 .objects
                                 .get_or_create(product=product,
                                                price=product.price,
                                                availability=product.quantity,
                                                owner=product.seller.customer))


def paginate(request, qers, limit=3):
    paginated_qers = Paginator(qers, limit)
    page_num = request.GET.get('page')
    return paginated_qers.get_page(page_num)


def is_htmx(request, boost_check=True):
    hx_boost = request.headers.get('Hx-Boosted')
    hx_request = request.headers.get('Hx-Request')

    if boost_check and hx_boost:
        return False

    elif boost_check and not hx_boost and hx_request:
        return True
