from django.contrib.auth.models import Group

from .models import Chats


def get_or_create_chat(user_req, user_pag):
    """Creates or gets the chat for a group of two users, return group name"""
    sorted_ids = [*map(str, sorted([user_pag.id, user_req.id]))]
    group_name = "Group" + "_".join(sorted_ids)
    group, created = Group.objects.get_or_create(name=group_name)
    group.user_set.add(user_req, user_pag)
    chat, created = (Chats
                     .objects
                     .get_or_create(
                         group=group,
                         name=str(group_name) + "_chat"
                     ))
    return group_name
