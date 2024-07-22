from django.urls import path, include

from .views import (LoginUser, RegisterUser, logoutuser,
                    UserShow, EditUser, RequestsCheck,
                    ProductsMaintain, updateOrder)


urlpatterns = [
    path("", LoginUser.as_view(), name="logpage"),
    path('accounts/', include("allauth.urls")),
    path("registerpage", RegisterUser.as_view(), name="regpage"),
    path("logout", logoutuser, name="logout"),
    path('profile/<slug:username>/', UserShow.as_view(), name="post"),
    path('profile/<slug:username>/edit', EditUser.as_view(), name="edit"),
    path('profile/warehouse', ProductsMaintain.as_view(), name='products-maintain'),
    path('profile/warehouse/requests_check', RequestsCheck.as_view(), name='requests-check'),
    path('update_order/', updateOrder, name='update_order'),
]