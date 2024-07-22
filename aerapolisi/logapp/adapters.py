from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from shop.models import Customer, Favourite


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        main_act = super(MySocialAccountAdapter, self).save_user(
            request, sociallogin, form
        )
        user = main_act
        customer_name = str(user.username) + '_customer'
        customer, created = (Customer
                             .objects
                             .get_or_create(user=user,
                                            name=customer_name,
                                            email=user.email))
        Favourite.objects.create(customer=customer)
        return user
