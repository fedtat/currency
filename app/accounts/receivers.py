from accounts.models import User

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def pre_save_user_first_name_change(sender, instance, **kwargs):
    if instance.first_name:
        instance.first_name = instance.first_name.capitalize()


@receiver(pre_save, sender=User)
def pre_save_user_last_name_change(sender, instance, **kwargs):
    if instance.last_name:
        instance.last_name = instance.last_name.capitalize()


@receiver(pre_save, sender=User)
def pre_save_user_phone_change(sender, instance, **kwargs):
    if instance.phone:
        instance.phone = ''.join(filter(str.isdigit, instance.phone))


@receiver(pre_save, sender=User)
def pre_save_user_email_change(sender, instance, **kwargs):
    if instance.email:
        instance.email = instance.email.lower()


@receiver(post_save, sender=User)
def post_save_user(sender, instance, **kwargs):
    pass
