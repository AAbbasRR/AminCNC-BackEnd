from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

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
    status_choices = [
        ('CNS', 'لغو شده'),
        ('SUC', 'تحویل داده شده'),
        ('AWC', 'در انتظار تایید'),
        ('PRE', 'در حال آماده سازی'),
    ]
    status = models.CharField(
        max_length=3,
        choices=status_choices,
        null=False,
        default='AWC',
        verbose_name='وضعیت'
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
    description = models.TextField(
        null=True,
        default='خالی',
        verbose_name='توضیحات کاربر قبل از انجام سفارش'
    )
    admin_description = models.TextField(
        null=True,
        blank=True,
        verbose_name='توضیحات ادمین'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(Orders)
        Permission.objects.get_or_create(codename='can_confirm_order', name='Can Confirm Order', content_type=content_type)

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
    payable_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name="جمع قیمت قابل پرداخت(تومان)"
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name="مبلغ تخفیف خورده"
    )

    def __str__(self) -> str:
        return f"product {self.order.pk} - {self.product.pk}"
