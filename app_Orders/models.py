from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

from app_User.models import Address
from app_Product.models import Delivery_mode, MaterialModel

import uuid


class Orders(models.Model):
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = f"{verbose_name}ات"

    user_and_address = models.ForeignKey(
        Address,
        related_name='order_address_user',
        on_delete=models.DO_NOTHING,
        verbose_name='کاربر و آدرس گیرنده'
    )
    products = models.ManyToManyField(
        MaterialModel,
        related_name='order_product',
        through='ProductsModel',
        verbose_name='محصولات'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name="کل مبلغ سفارش(تومان)"
    )
    submit_date = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
        verbose_name='تاریخ ثبت سفارش'
    )
    delivery_status = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name='وضعیت ارسال'
    )
    tracking_code = models.CharField(
        max_length=12,
        default=str(uuid.uuid4()).split('-')[-1],
        unique=True,
        null=False,
        blank=False,
        verbose_name='کد رهگیری'
    )
    delivery_mode = models.ForeignKey(
        Delivery_mode,
        related_name='order_delivery',
        on_delete=models.CASCADE,
        verbose_name='نوع ارسال'
    )

    def __str__(self) -> str:
        return f"{self.user_and_address.user.mobile_number} - {self.tracking_code} - {self.total_price}"


class ProductsModel(models.Model):
    class Meta:
        verbose_name = "محصول سفارش داده شده"
        verbose_name_plural = "محصولات سفارش داده شده"

    order = models.ForeignKey(
        Orders,
        related_name='order_order',
        on_delete=models.DO_NOTHING,
        verbose_name='سفارش'
    )
    product = models.ForeignKey(
        MaterialModel,
        related_name='order_product_material',
        on_delete=models.DO_NOTHING,
        verbose_name='محصول'
    )
    number = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        null=False,
        blank=False,
        verbose_name='تعداد'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name="جمع قیمت(تومان)"
    )
