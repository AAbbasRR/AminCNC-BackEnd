from django.db import models
from django.utils import timezone

from app_User.models import User

import uuid


class Service(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='کاربر'
    )
    description_service = models.TextField(
        null=False,
        blank=False,
        verbose_name='توضیحات درخواست'
    )
    image = models.ImageField(
        null=True,
        blank=True,
        verbose_name='عکس'
    )
    submit_date = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
        verbose_name='تاریخ ثبت'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name="مبلغ پرداختی(تومان)"
    )
    payment_description = models.TextField(
        null=True,
        blank=True,
        verbose_name='توضیحات پرداخت'
    )
    status_choices = [
        ('CNS', 'لغو شده'),
        ('SUC', 'تحویل داده شده'),
        ('PAY', 'در انتظار پرداخت'),
        ('ANS', 'در انتظار پاسخ'),
        ('PRP', 'در حال آماده سازی'),
    ]
    status = models.CharField(
        max_length=3,
        choices=status_choices,
        null=False,
        default='ANS',
        verbose_name='وضعیت'
    )

    def __str__(self) -> str:
        return f"{self.user.mobile_number} - {self.status}"

