from django.db import models


class ProductOffersManager(models.Manager):
    def initialize_offer(self, product):
        """
        Initialize a product offer with default values.
        """
        offer = self.create(
            product=product,
            price=product.price,
            availability=product.quantity,
            owner=product.seller.customer
        )
        return offer
