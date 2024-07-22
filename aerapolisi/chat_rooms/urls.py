from django.urls import path

from .views import ChatRoom


urlpatterns = [
    path("<slug:seller_name>", ChatRoom.as_view(), name="seller"),
]
