from django.db import models
from django.contrib.auth.models import Group

from logapp.models import User
from shop.models import Products


class Chats(models.Model):
    "Chat groups with unique name"

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)

    def get_last_10(self):
        messages = Messages.objects.filter(chat=self.pk).order_by("created")
        result = list(messages)
        return result

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"


class Messages(models.Model):
    "Messages for chat groups"

    chat = models.ForeignKey(Chats, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200, blank=False, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    product = models.ForeignKey(
        Products, null=True, blank=True, on_delete=models.SET_DEFAULT, default=""
    )

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
