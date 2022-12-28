from django.db.models.signals import post_save
from django.db.models import F
from django.dispatch import receiver
from django.core.management import call_command

from app_Settings.models import SiteOptions
from app_User.utils import Redis

from .models import ProductsModel


@receiver(post_save, sender=ProductsModel)
def create_order_product_handler(sender, instance, **kwargs):
    if kwargs['created']:
        redis_management = Redis("admin", "settings")
        if redis_management.exists():
            low_off = redis_management.get_value() == "True"
        else:
            siteOptions = SiteOptions.objects.first()
            if siteOptions is not None:
                low_off = siteOptions.low_off_product_inventory
                siteOptions.low_off_product_inventory = low_off
                siteOptions.save()
            else:
                call_command("createoptions")
                low_off = True
        if low_off is True:
            instance.product.number = F("number") - instance.number
            instance.product.save()
