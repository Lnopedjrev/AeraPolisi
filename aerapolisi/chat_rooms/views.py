from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.models import Group

from main.services import is_htmx
from logapp.models import User
from shop.models import Products
from django.db import transaction
from .models import Chats


class ChatRoom(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "seller"
    login_url = reverse_lazy("logpage")

    def get_template_names(self):
        """Check if the loading page hast htmx"""
        if is_htmx(self.request):
            return "chat_rooms/seller-products.html"
        else:
            return "chat_rooms/chat-template.html"

    def get_object(self, queryset=None, **kwargs):
        """Returns the user instance of the interlocutor(seller)
        and creates or get chat group"""
        user_req = self.request.user
        user_pag = self.user_pag
        self.group_name = self.get_or_create_chat(user_req, user_pag)

        return user_pag

    def get_or_create_chat(self, user_req, user_pag):
        """Creates or gets the chat for a group of two users, return group name"""
        sorted_ids = [*map(str, sorted([user_pag.id, user_req.id]))]
        group_name = "Group" + "_".join(sorted_ids)

        with transaction.atomic():
            group, created = Group.objects.get_or_create(name=group_name)
            group.user_set.add(user_req, user_pag)
            chat, created = Chats.objects.get_or_create(
                group=group, name=str(group_name) + "_chat"
            )
        return group_name

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get products of the seller and returns it in paginated form"""
        default_context = super().get_context_data(**kwargs)
        seller = self.user_pag

        page = self.request.GET.get("page")
        products = Products.objects.filter(
            seller=seller, ontest=False
        ).prefetch_related("productsgallery_set")
        paginator = Paginator(products, 5)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        title = seller.username.upper() + "_chat"
        view_context = dict(
            title=title,
            group=self.group_name,
            products=products,
            type="chat",
            aginate_except=True,
        )
        return {**default_context, **view_context}

    def test_func(self) -> bool | None:
        """Verifies that the requesting user and interlocutor
        aren't the same person"""
        self.user_pag = User.objects.get(username=self.kwargs["seller_name"])

        return not self.user_pag == self.request.user
