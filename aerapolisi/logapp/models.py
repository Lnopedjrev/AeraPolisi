from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

import datetime
from dateutil.relativedelta import relativedelta


class User(AbstractUser):
    """The modified user model"""
    GENDER_CHOICES = [
                    ("0", 'FEMALE'),
                    ("1", 'MALE')
    ]
    gender_choice = models.CharField(max_length=30, choices=GENDER_CHOICES,
                                     default=0, verbose_name="GENDER")
    date_birth = models.DateField(null=True)
    image = models.ImageField(upload_to="images/users-images",
                              default='default_logo_image.jpg')
    description = models.TextField(blank=True)
    balance = models.FloatField(default=0)

    def get_gender(self):
        return dict(User.GENDER_CHOICES)[self.gender_choice]

    def get_age(self):
        return relativedelta(datetime.date.today(), self.date_birth).years

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("post", kwargs={"username": self.username})
