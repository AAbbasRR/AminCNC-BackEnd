from django.db import models

from app_User.utils import Redis


class SiteOptions(models.Model):
    class Meta:
        verbose_name = 'ایتم تنظیم سایت'
        verbose_name_plural = 'تنظیمات سایت'

    phone_number = models.CharField(
        max_length=30,
        null=False,
        verbose_name='شماره تماس'
    )
    address = models.TextField(
        null=False,
        verbose_name='ادرس'
    )
    week_hours_work = models.CharField(
        max_length=10,
        null=False,
        verbose_name='ساعت کاری شنبه الی چهارشنبه'
    )
    weekend_hours_work = models.CharField(
        max_length=10,
        null=False,
        verbose_name='ساعت کاری پنجشنبه'
    )
    low_off_product_inventory = models.BooleanField(
        default=True,
        null=False,
        verbose_name='کم کردن موجودی محصولات بعد از ثبت سفارش کاربران'
    )

    def __str__(self) -> str:
        return self.phone_number

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        redis_management = Redis("admin", "settings")
        redis_management.set_value(str(self.low_off_product_inventory))
        return super(SiteOptions, self).save(force_insert, force_update, using, update_fields)
