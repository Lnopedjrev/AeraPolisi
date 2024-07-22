from django.urls import path

from .views import ProductsOnTestList

urlpatterns = [
    path("products_on_check", ProductsOnTestList.as_view(), name="managing-products"),
]
