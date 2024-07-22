from django.db import models
from django.urls import reverse
from django.contrib.auth.models import Group

from logapp.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True,
                                blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    online_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    descriptions = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'ProductsCategories'


class Products(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=100, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    service = models.BooleanField(default=False, null=True, blank=False)
    seller = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    categories = models.ManyToManyField(ProductCategory)
    ontest = models.BooleanField(default=True)

    def __str__(self):
        return '%s - %s' % (self.name, self.pk)

    def get_first_image(self):
        return self.productsgallery_set.first().image.url

    def get_absolute_url(self):
        return reverse("product-detailed", kwargs={"id": self.id})

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['created']


class ProductOffers(models.Model):
    product = models.ForeignKey(Products, default=None,
                                on_delete=models.CASCADE)
    price = models.FloatField(blank=True, null=True, default=100)
    owner = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    availability = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s - %s' % (self.product.name, self.owner, self.created)

    def get_active(self):
        if self.availability <= 0:
            self.is_active = False
            self.save()
        return self.is_active

    def get_edit_url(self):
        return reverse("edit-offer", kwargs={"id": self.id})

    def get_checkout_url(self):
        return reverse("product-checkout", kwargs={"id": self.id})

    class Meta:
        verbose_name = 'ProductOffer'
        verbose_name_plural = 'ProductOffers'
        ordering = ['created']


class ProductsGallery(models.Model):
    product = models.ForeignKey(Products, default=None,
                                on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='products-images')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.product.name, self.image)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'ProductsGallery'
        ordering = ['created']


class Favourite(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.pk, self.customer)


class FavouriteItem(models.Model):
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE, null=True)
    favourite = models.ForeignKey(Favourite,
                                  on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.name


class OrderInfo(models.Model):
    offer = models.ForeignKey(ProductOffers,
                              on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    date_odered = models.DateTimeField(auto_now_add=True)
    payee = models.ForeignKey(Customer, on_delete=models.SET_NULL,
                              blank=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self) -> str:
        return '{} - {}'.format(self.offer.product, self.payee)


class ShippingAdress(models.Model):
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE,
                              blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return '{} - {}'.format(self.order.pk, self.order.payee)


class OwnerGroup(Group):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Groups'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class OrderRequests(models.Model):
    last_order = models.ForeignKey(OrderInfo, on_delete=models.SET_NULL,
                                   blank=True, null=True)
    number = models.IntegerField(default=0)
    date_requested = models.DateTimeField(auto_now_add=True)
    shipping = models.ForeignKey(ShippingAdress, on_delete=models.SET_NULL,
                                 blank=True, null=True)

    def __str__(self) -> str:
        return '{} - {}'.format(self.last_order.payee, self.date_requested)

    class Meta:
        verbose_name = 'OrderRequest'
        verbose_name_plural = 'Requests'
        ordering = ['date_requested']
