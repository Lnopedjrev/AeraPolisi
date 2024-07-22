from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import * 


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity',
                    'price', 'service',
                    'ontest', "get_object_image")
    list_display_links = ('id', 'name')
    search_fields = ('name', 'price')
    list_editable = ('ontest',)
    readonly_fields = ('get_object_image', 'created', 'updated')

    def get_object_image(self, object):
        if object.get_first_image():
            return mark_safe(f"<img src='{object.get_first_image()}' width=50>")

admin.site.register(Products, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Favourite)
admin.site.register(FavouriteItem)
admin.site.register(ProductsGallery)
admin.site.register(OrderInfo)
admin.site.register(ShippingAdress)
admin.site.register(ProductCategory)
admin.site.register(OwnerGroup)
admin.site.register(ProductOffers)
admin.site.register(OrderRequests)
# Register your models here.
