from contextlib import nullcontext

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.html import mark_safe

from app_Material.models import Size, Material

import uuid


class Discount(models.Model):
    class Meta:
        verbose_name = "تخفیف"
        verbose_name_plural = f"{verbose_name} ها"
        ordering = ['number']

    number = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=False,
        blank=False,
        verbose_name='تعداد تخفیف',
    )
    percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=False,
        blank=False,
        verbose_name='درصد اعمال تخفیف روی قیمت'
    )

    def __str__(self) -> str:
        return f"{self.percent} درصد تخفیف برای تعداد بیشتر از {self.number}"


class Delivery_mode(models.Model):
    class Meta:
        verbose_name = "حالت ارسال"
        verbose_name_plural = f"{verbose_name} ها"

    mode_name = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name='نام نوع ارسال'
    )
    price = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        default='متغیر',
        verbose_name='قیمت ارسال(تومان)'
    )

    def __str__(self) -> str:
        return self.mode_name


class ProductPreparationTime(models.Model):
    class Meta:
        verbose_name = "زمان تحویل محصول"
        verbose_name_plural = f"{verbose_name}ات"

    number = models.IntegerField(
        null=False,
        verbose_name=' تعداد محصول'
    )
    preparation_time = models.IntegerField(
        null=False,
        verbose_name='زمان آماده سازی(روز کاری)'
    )

    def __str__(self) -> str:
        return f"{self.preparation_time} روز کاری برای آماده سازی {self.number} تعداد محصول"


class Product(models.Model):
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = f"{verbose_name}ات"
        ordering = ['-created_date']

    name = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name='نام محصول'
    )
    productId = models.CharField(
        max_length=12,
        default=str(uuid.uuid4()).split('-')[-1],
        unique=True,
        null=False,
        blank=False,
        verbose_name='کد رهگیری'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        verbose_name='لینک انگلیسی'
    )
    preparation_time = models.ForeignKey(
        ProductPreparationTime,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='زمان آماده سازی'
    )
    created_date = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
        verbose_name='تاریخ ایجاد'
    )
    short_description = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='توضیحات کوتاه'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='توضیحات تکمیلی'
    )
    materials = models.ManyToManyField(
        Material,
        through='MaterialModel',
        verbose_name='جنس-سایز-قیمت'
    )
    discounts = models.ManyToManyField(
        Discount,
        related_name='product_discounts',
        verbose_name='تخفیف ها'
    )
    show_in_index = models.BooleanField(
        default=False,
        verbose_name="نمایش در صفحه اصلی سایت"
    )

    def __str__(self) -> str:
        return self.name


class Picture(models.Model):
    class Meta:
        verbose_name = "عکس"
        verbose_name_plural = f"{verbose_name} ها"

    product = models.ForeignKey(
        Product,
        related_name='product_image',
        on_delete=models.CASCADE,
        verbose_name='محصول'
    )
    picture = models.ImageField(
        upload_to='products/images/',
        null=False,
        blank=False,
        verbose_name='عکس'
    )

    def __str__(self):
        return self.picture.url

    def get_image_tag(self):
        return mark_safe('<img src="/media/%s"  width="150" />' % self.picture)


class MaterialModel(models.Model):
    class Meta:
        verbose_name = "سایز و جنس"
        verbose_name_plural = f"سایز ها و جنس ها"

    product = models.ForeignKey(
        Product,
        related_name='product_product',
        on_delete=models.DO_NOTHING,
        verbose_name='محصول'
    )
    material = models.ForeignKey(
        Material,
        related_name='product_material',
        on_delete=models.DO_NOTHING,
        verbose_name='نوع ماده'
    )
    size = models.ForeignKey(
        Size,
        related_name='product_size',
        on_delete=models.DO_NOTHING,
        verbose_name='اندازه'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name="قیمت واحد(تومان)"
    )
    number = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        null=False,
        blank=False,
        verbose_name='تعداد موجود'
    )

    def __str__(self) -> str:
        return f"{self.material} - {self.size}"
