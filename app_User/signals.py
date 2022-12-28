from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from .models import User
from .utils import Manage_SMS_Portal


@receiver(post_save, sender=User)
def create_user_handler(sender, instance, **kwargs):
    if kwargs['created']:
        Token.objects.create(
            user=instance
        )
        if instance.is_active is False:
            manage_sms_obj = Manage_SMS_Portal(instance.mobile_number)
            manage_sms_obj.send_otp_code()
