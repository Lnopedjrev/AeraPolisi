from django.urls import path
from .views import (
    Shop,
    favourite,
    SupposeProduct,
    ProductShow,
    ProductPurchase,
    ProductCheckout,
)
from logapp.views import EditProduct, EditOffer

urlpatterns = [
    path("", Shop.as_view(), name="shop"),
    path("favourite", favourite, name="favourite"),
    path("create_product", SupposeProduct.as_view(), name="product-create"),
    path("product/<int:id>/", ProductShow.as_view(), name="product-detailed"),
    path(
        "product/purchase/offer/<int:id>",
        ProductPurchase.as_view(),
        name="product-purchase",
    ),
    path("product/offer/<int:id>/edit", EditOffer.as_view(), name="edit-offer"),
    path("product/<int:id>/edit", EditProduct.as_view(), name="edit-product"),
    path(
        "product/offer/checkout/<int:id>",
        ProductCheckout.as_view(),
        name="product-checkout",
    ),
]
