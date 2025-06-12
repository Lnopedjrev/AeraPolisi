from django.urls import path

from .views import MainPageView, updateItem

urlpatterns = [
    path("", MainPageView.as_view(), name="main"),
    path("update_item/", updateItem, name="update_item"),  # remove it
]
