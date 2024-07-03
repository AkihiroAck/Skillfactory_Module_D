from django.db.models.signals import m2m_changed, post_save
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from django.contrib.auth.models import Group
from django.contrib.auth.models import User


@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    default_group_name = 'users'
    default_group = Group.objects.get(name=default_group_name)
    user.groups.add(default_group)
    user.save()
