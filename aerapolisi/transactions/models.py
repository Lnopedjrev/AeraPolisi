from django.db import models
from logapp.models import User


class UserPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500,
                                          null=True,
                                          blank=True)
