from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password


@receiver(pre_save, sender=User)
def hash_user_password(sender, instance, **kwargs):
    if instance._state.adding:
        instance.password = make_password(instance.password)
