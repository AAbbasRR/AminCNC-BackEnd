from django.db import models
from django.utils import timezone

from app_User.models import User
from app_Orders.models import Orders


class PaymentHistory(models.Model):
    class Meta:
        verbose_name = "تاریخچه تراکنش"
        verbose_name_plural = f"{verbose_name} ها"

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="کاربر"
    )
    order = models.ForeignKey(
        Orders,
        on_delete=models.PROTECT,
        verbose_name="سفارش"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name="مبلغ پرداخت شده(تومان)"
    )
    date = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
        verbose_name='تاریخ ثبت سفارش'
    )
    status_choices = [
        ('CNS', 'لغو شده'),
        ('SUC', 'پرداخت شده'),
    ]
    status = models.CharField(
        max_length=3,
        choices=status_choices,
        null=False,
        default='CNS',
        verbose_name='وضعیت'
    )
    portal_choices = [
        ('ZPL', 'زرینپال'),
    ]
    portal = models.CharField(
        max_length=3,
        choices=portal_choices,
        null=False,
        default='ZPL',
        verbose_name='درگاه پرداخت'
    )
    ref_id = models.CharField(
        max_length=50,
        null=False,
        unique=True,
        verbose_name='کد پیگیری'
    )

    def __str__(self) -> str:
        return f"{self.date} - {self.price}"
